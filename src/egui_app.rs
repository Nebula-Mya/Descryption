use eframe::egui;
use std::sync::mpsc;

/// The enum for toggling which debug UI is currently visible.
#[derive(Debug, PartialEq)]
enum DebugUi {
    None,
    Settings,
    Memory,
    Texture,
    Inspection,
}

// We derive Deserialize/Serialize so we can persist app state on shutdown.
/// The structure that represents the GUI app.
/// The [`update()`](eframe::App::update), [`new()`](EguiApp::new), and [`save()`](eframe::App::save) methods define the app's behavior.
#[derive(serde::Deserialize, serde::Serialize)]
#[serde(default)] // if we add new fields, give them default values when deserializing old state
pub struct EguiApp {
    /// The debug UI currently visible.
    /// Only matters in when run in debug mode.
    /// Always [`DebugUi::None`] on launch.
    #[serde(skip)]
    debug_uis: DebugUi,

    /// The message recieved most recently
    #[serde(skip)]
    recent_msg: String,

    /// The user's input text
    #[serde(skip)]
    current_input: String,

    /// The sender for the input channel
    #[serde(skip)]
    input_tx: Option<mpsc::Sender<String>>,

    /// The receiver for the output channel
    #[serde(skip)]
    output_rx: Option<mpsc::Receiver<String>>,

    /// The sender for the context channel
    #[serde(skip)]
    context_tx: Option<mpsc::Sender<egui::Context>>,

    /// Flag for loading fonts
    #[serde(skip)]
    load_fonts: bool,
}

impl Default for EguiApp {
    fn default() -> Self {
        // get path for the cache directory and the png saved by nannou
        // let project_dirs = ProjectDirs::from(
        //     "",
        //     "Shark Pauldrons",
        //     "nannou application",
        // )
        // .expect("Could not find cache directory");

        // let cache_dir = project_dirs.cache_dir().to_owned();

        Self {
            debug_uis: DebugUi::None,
            recent_msg: "".to_string(),
            current_input: "".to_string(),
            input_tx: None,
            output_rx: None,
            context_tx: None,
            load_fonts: true,
        }
    }
}

impl EguiApp {
    /// Called once before the first frame.
    /// Responsible for initializing the app.
    pub fn new(
        cc: &eframe::CreationContext<'_>,
        input_tx: mpsc::Sender<String>,
        output_rx: mpsc::Receiver<String>,
        context_tx: mpsc::Sender<egui::Context>,
    ) -> Self {
        // load previous app state if possible
        if let Some(storage) = cc.storage {
            let old_data: Self = eframe::get_value(storage, eframe::APP_KEY).unwrap_or_default();
            return Self {
                input_tx: Some(input_tx),
                output_rx: Some(output_rx),
                context_tx: Some(context_tx),
                ..old_data
            };
        }

        // if no previous app state, use the default config
        Self {
            input_tx: Some(input_tx),
            output_rx: Some(output_rx),
            context_tx: Some(context_tx),
            ..Default::default()
        }
    }
}

impl eframe::App for EguiApp {
    fn save(&mut self, storage: &mut dyn eframe::Storage) {
        // save current app state to be loaded on next launch
        eframe::set_value(storage, eframe::APP_KEY, self);
    }

    fn update(&mut self, ctx: &egui::Context, _frame: &mut eframe::Frame) {
        // load Consolas
        if self.load_fonts {
            let mut fonts = egui::FontDefinitions::default();

            fonts.font_data.insert(
                "Consolas".to_owned(),
                std::sync::Arc::new(egui::FontData::from_static(
                    include_bytes!("../assets/consola.ttf"),
                )),
            );

            // make default for monospaced
            fonts
                .families
                .get_mut(&egui::FontFamily::Monospace)
                .unwrap()
                .insert(0, "Consolas".to_owned());

            ctx.set_fonts(fonts);

            self.load_fonts = false;
        }

        // close if Ctrl+D
        if ctx.input(|i| i.key_pressed(egui::Key::D) && i.modifiers.ctrl) {
            ctx.send_viewport_cmd(egui::ViewportCommand::Close);
        }

        // send context to secondary thread
        let _ = self
            .context_tx
            .as_ref()
            .unwrap()
            .send(ctx.clone());

        // get output from secondary thread if updated
        if let Ok(msg) = self
            .output_rx
            .as_ref()
            .unwrap()
            .try_recv()
        {
            self.recent_msg = msg;
        }

        // bottom panel, only holds useful information if in debug mode, may not display at all in release, TBD
        egui::TopBottomPanel::bottom("bottom_panel")
            .resizable(true)
            .default_height(1.0)
            .show(ctx, |ui| {
                if cfg!(debug_assertions) {
                    // select a debug ui to show
                    egui::ComboBox::from_label("Debug Menu")
                        .selected_text(format!("{:?}", self.debug_uis))
                        .show_ui(ui, |ui| {
                            ui.selectable_value(
                                &mut self.debug_uis,
                                DebugUi::None,
                                "None",
                            );
                            ui.selectable_value(
                                &mut self.debug_uis,
                                DebugUi::Settings,
                                "Settings",
                            );
                            ui.selectable_value(
                                &mut self.debug_uis,
                                DebugUi::Inspection,
                                "Inspection",
                            );
                            ui.selectable_value(
                                &mut self.debug_uis,
                                DebugUi::Texture,
                                "Texture",
                            );
                            ui.selectable_value(
                                &mut self.debug_uis,
                                DebugUi::Memory,
                                "Memory",
                            );
                        });

                    // display the selected debug ui
                    match self.debug_uis {
                        DebugUi::None => {}
                        DebugUi::Settings => {
                            ctx.settings_ui(ui);
                        }
                        DebugUi::Inspection => {
                            ctx.inspection_ui(ui);
                        }
                        DebugUi::Texture => {
                            ctx.texture_ui(ui);
                        }
                        DebugUi::Memory => {
                            ctx.memory_ui(ui);
                        }
                    }
                };
            });

        // the terminal display
        egui::CentralPanel::default().show(ctx, |ui| {
            let mut text_full = self.recent_msg.clone() + &self.current_input;

            let text_response = ui
                .scope(|ui| {
                    egui::ScrollArea::vertical()
                        .stick_to_bottom(true)
                        .scroll_bar_visibility(egui::scroll_area::ScrollBarVisibility::AlwaysHidden)
                        .show(ui, |ui| {
                            ui.add_sized(
                                ui.available_size(),
                                egui::TextEdit::multiline(&mut text_full)
                                    .frame(false)
                                    .lock_focus(true)
                                    .font(egui::FontId::new(
                                        16.0,
                                        egui::FontFamily::Monospace,
                                    )),
                            )
                        })
                        .inner
                })
                .inner;

            // restrict cursor to input portion
            if let Some(mut state) = egui::TextEdit::load_state(ui.ctx(), text_response.id) {
                if let Some(mut range) = state.cursor.char_range() {
                    range.primary.index = std::cmp::max(
                        range.primary.index,
                        self.recent_msg.chars().count(),
                    );
                    range.secondary.index = std::cmp::max(
                        range.secondary.index,
                        self.recent_msg.chars().count(),
                    );
                    // let ccursor = egui::text::CCursor::new(0);
                    state.cursor.set_char_range(Some(range));
                    state.store(ui.ctx(), text_response.id)
                }
            }

            self.current_input =
                text_full[std::cmp::min(self.recent_msg.len(), text_full.len())..].to_string();
        });

        // send user input
        if self.current_input.contains('\n') {
            let input_str = self
                .current_input
                .split('\n')
                .next()
                .unwrap()
                .to_string();
            let _ = self
                .input_tx
                .as_ref()
                .unwrap()
                .send(input_str);
            self.current_input.clear();
        }
    }
}
