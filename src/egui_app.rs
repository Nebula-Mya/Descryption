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

    /// The number of times [`update()`](eframe::App::update) has been ran, including the current iteration.
    /// Only used for calling [nannou](crate::nannou_app::Model) on launch and for debugging.
    /// Always `0` on launch
    #[serde(skip)]
    tick_count: u32,

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
            tick_count: 0,
            recent_msg: "".to_string(),
            current_input: "".to_string(),
            input_tx: None,
            output_rx: None,
            context_tx: None,
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
        // REMINDME: not working; can't give correct channels in default
        // if let Some(storage) = cc.storage {
        //     return eframe::get_value(storage, eframe::APP_KEY).unwrap_or_default();
        // }

        // if no previous app state, use the default config
        Self {
            input_tx: Some(input_tx),
            output_rx: Some(output_rx),
            context_tx: Some(context_tx),
            // ..Default::default()
            debug_uis: DebugUi::None,
            tick_count: 0,
            recent_msg: "".to_string(),
            current_input: "".to_string(),
        }
    }
}

impl eframe::App for EguiApp {
    fn save(&mut self, storage: &mut dyn eframe::Storage) {
        // save current app state to be loaded on next launch
        eframe::set_value(storage, eframe::APP_KEY, self);
    }

    fn update(&mut self, ctx: &egui::Context, _frame: &mut eframe::Frame) {
        self.tick_count += 1;

        let _ = self
            .context_tx
            .as_ref()
            .unwrap()
            .send(ctx.clone());

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

                // this is always connected to the bottom of the window
                ui.with_layout(
                    egui::Layout::bottom_up(egui::Align::LEFT),
                    |ui| {
                        powered_by_egui_and_nannou(ui);
                        egui::warn_if_debug_build(ui);
                        if cfg!(debug_assertions) {
                            ui.label(format!("tick: {}", self.tick_count));
                        }
                    },
                );
            });

        // the main region of the app's GUI
        egui::CentralPanel::default().show(ctx, |ui| {
            let mut text_full = self.recent_msg.clone() + &self.current_input;

            let text_response = ui.text_edit_multiline(&mut text_full);

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
    }
}

/// Helper function to draw credit text at bottom. Honestly quite unnecessary.
fn powered_by_egui_and_nannou(ui: &mut egui::Ui) {
    ui.horizontal(|ui| {
        ui.spacing_mut().item_spacing.x = 0.0;
        ui.label("Powered by ");
        ui.hyperlink_to("egui", "https://github.com/emilk/egui");
        ui.label(" and ");
        ui.hyperlink_to(
            "nannou",
            "https://github.com/nannou-org/nannou",
        );
        ui.label(".");
    });
}
