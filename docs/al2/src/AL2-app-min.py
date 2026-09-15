# いちばん小さい Gradio アプリ
# VS Code の右上の実行ボタン（三角）で実行すると、ブラウザに画面が開く
import gradio as gr


def make_message(name, size):
    """入力欄とスライダーの値を受け取り、画面に出す文を返す"""
    return f"{name} さんの {size} × {size} の迷路を作ります"


app = gr.Interface(
    fn=make_message,                                   # ボタンを押すと呼ばれる関数
    inputs=[
        gr.Textbox(label="名前", value="自分の名前"),
        gr.Slider(3, 10, value=5, step=1, label="迷路の大きさ"),
    ],
    outputs=gr.Textbox(label="結果"),
    title="迷路アプリ",
)

app.launch(inbrowser=True)                             # ブラウザを自動で開く
