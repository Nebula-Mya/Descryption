// TODO: revamp to reuse frame
use directories::ProjectDirs;
use eframe::egui;
use std::{
    path::PathBuf,
    sync::Arc,
};

// NOTE: may be dependent on font
const WIN_TITLE_HEIGHT: f32 = 32.7;

/// The enum for toggling which debug UI is currently visible.
#[derive(Debug, PartialEq)]
enum DebugUi {
    None,
    Settings,
    Memory,
    Texture,
    Inspection,
}

/// The enum for keeping track of what the single [file dialog](egui_file_dialog::FileDialog) instance is being used for.
#[derive(PartialEq)]
enum ExplorerState {
    /// The [file explorer](egui_file_dialog) is not being used.
    Closed,

    /// The [file explorer](egui_file_dialog) is being used to create a new save file.
    SaveAs,

    /// The [file explorer](egui_file_dialog) is being used to load an existing save file.
    Open,

    /// The [file explorer](egui_file_dialog) is being used to create a new png.
    Export,
}

/// The enum for keeping track of what [`Modal`] is being shown.
#[derive(PartialEq)]
enum Modals {
    /// No [modal](egui::containers::Modal) is being shown.
    None,

    /// The [modal](egui::containers::Modal) prompting user to confirm node deletion.
    Delete,

    /// The [modal](egui::containers::Modal) prompting user to rename a node.
    Rename,

    /// The [modal](egui::containers::Modal) informing the user that the file selected to load does not contain valid save data.
    BadOpen,
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
    tick_count: u32
}

impl Default for EguiApp {
    fn default() -> Self {
        // get path for the cache directory and the png saved by nannou
        let project_dirs = ProjectDirs::from(
            "",
            "Shark Pauldrons",
            "nannou application",
        )
        .expect("Could not find cache directory");

        let cache_dir = project_dirs.cache_dir().to_owned();

        Self {
            debug_uis: DebugUi::None,
            tick_count: 0,
        }
    }
}

impl EguiApp {
    /// Called once before the first frame.
    /// Responsible for initializing the app.
    pub fn new(cc: &eframe::CreationContext<'_>) -> Self {
        // load previous app state if possible
        if let Some(storage) = cc.storage {
            return eframe::get_value(storage, eframe::APP_KEY).unwrap_or_default();
        }

        // if no previous app state, use the default config
        Default::default()
    }
}

impl eframe::App for EguiApp {
    fn save(&mut self, storage: &mut dyn eframe::Storage) {
        // save current app state to be loaded on next launch
        eframe::set_value(storage, eframe::APP_KEY, self);
    }

    fn update(&mut self, ctx: &egui::Context, _frame: &mut eframe::Frame) {
        self.tick_count += 1;

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
            todo!();
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