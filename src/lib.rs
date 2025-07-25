#![warn(clippy::all, rust_2018_idioms)]
#![warn(missing_docs)]
//! A node based code art application built using [nannou] and [egui].

/// A generic result type that holds a boxed [error](std::error::Error)
pub type Result<T> = std::result::Result<T, Box<dyn std::error::Error>>;

mod egui_app;
pub use egui_app::EguiApp;