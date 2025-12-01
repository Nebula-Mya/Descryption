use std::sync::mpsc;

/// Test using message channels to emulate a terminal.
pub fn main(
    output_tx: mpsc::Sender<String>,
    input_rx: mpsc::Receiver<String>,
    context_rx: mpsc::Receiver<egui::Context>,
) -> () {
    let ctx = context_rx
        .recv()
        .expect("Context channel was dropped by the app.");

    // test io stream with echo
    let mut history = "$ echo ".to_string();
    let _ = output_tx.send(history.clone());
    loop {
        let msg = input_rx
            .recv()
            .expect("Input channel was dropped by the app.");

        history.push_str(&format!("{msg}\n{msg}\n$ echo "));
        let _ = output_tx.send(history.clone());

        if msg == "exit".to_owned() {
            ctx.send_viewport_cmd(egui::ViewportCommand::Close);
        }
    }
}
