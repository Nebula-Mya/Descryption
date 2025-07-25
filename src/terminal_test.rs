use std::sync::mpsc;
// use egui::Context;

/// Test using message channels to emulate a terminal.
pub fn main(
    output_tx: mpsc::Sender<String>,
    input_rx: mpsc::Receiver<String>,
    _context_rx: mpsc::Receiver<egui::Context>,
) -> () {
    // let _ = output_tx.send("Hello world!".to_string());

    // let ctx = context_rx.recv().expect("Context channel was dropped by the app.");

    // test io stream with echo
    let mut history = "$ echo ".to_string();
    let _ = output_tx.send(history.clone());
    loop {
        if let Ok(msg) = input_rx.recv() {
            history.push_str(&format!("{msg}\n{msg}\n$ echo "));
            let _ = output_tx.send(history.clone());
        }
    }
    // ctx.send_viewport_cmd(egui::ViewportCommand::Close);
}
