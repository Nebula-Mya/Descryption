use std::{
    sync::mpsc
};
use egui::Context;

/// Test using message channels to emulate a terminal.
pub fn main (output_tx: mpsc::Sender<String>, input_rx: mpsc::Receiver<String>, context_rx: mpsc::Receiver<egui::Context>) -> () {
    let _ = output_tx.send("Hello world!".to_string());

    let ctx = context_rx.recv().expect("Context channel was dropped by the app.");

    //TODO: test getting input and sending output
}