#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")] // hide console window on Windows in release

use descryption::{terminal_fn, EguiApp};

use std::{sync::mpsc, thread};

fn main() {
    // Log to stderr (if ran with `RUST_LOG=debug`)
    env_logger::init();

    // set options for app
    let native_options = eframe::NativeOptions {
        viewport: egui::ViewportBuilder::default()
            .with_inner_size([400.0, 300.0])
            .with_min_inner_size([300.0, 220.0])
            .with_icon(
                // this icon is temporary
                eframe::icon_data::from_png_bytes(&include_bytes!("../assets/icon-128.png")[..])
                    .expect("Failed to load icon"),
            )
            .with_resizable(true),
        ..Default::default()
    };

    let (input_tx, input_rx) = mpsc::channel::<String>();
    let (output_tx, output_rx) = mpsc::channel::<String>();
    let (context_tx, context_rx) = mpsc::channel::<egui::Context>();

    thread::spawn(move || {
        // run terminal emulation in alt thread
        terminal_fn(output_tx, input_rx, context_rx);
    });

    // run app until close or error
    if let Err(err) = eframe::run_native(
        "Descryption",
        native_options,
        Box::new(|cc| {
            Ok(Box::new(EguiApp::new(
                cc, input_tx, output_rx, context_tx,
            )))
        }),
    ) {
        println!("{err}");
        std::process::exit(1);
    };
}
