import os
import streamlit as st
import streamlit.components.v1 as components
from google import genai
from google.genai import types

# =====================================
# ページ設定
# =====================================

st.set_page_config(
    page_title="Python学習支援チャットボット",
    page_icon="🐍",
    layout="centered"
)

st.title("🐍 Python学習支援チャットボット")
st.write("AIと一緒にPythonを学ぼう！")

# =====================================
# APIキー確認
# =====================================

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    try:
        api_key = st.secrets.get("GEMINI_API_KEY")
    except Exception:
        api_key = None

if not api_key:
    st.error(
        "APIキーが設定されていません。"
        "Streamlit Secrets または環境変数を確認してください。"
    )
    st.stop()

# =====================================
# Geminiクライアント
# =====================================

@st.cache_resource
def get_client(key):
    return genai.Client(
        api_key=key,
        http_options={"timeout": 60000}
    )

client = get_client(api_key)

# =====================================
# Pythonコード実行エリア
# =====================================

st.divider()
st.header("🧪 Pythonコードを試す")
st.write("コードを書いて、実行結果を確認しよう！")

components.html(
    r"""
    <div style="font-family:sans-serif;">
      <textarea id="code"
        aria-label="Pythonコードを入力"
        style="box-sizing:border-box;width:100%;height:180px;
        font-family:monospace;padding:10px;"
        placeholder='例：print("こんにちは！")'>print("こんにちは！")</textarea>

      <button id="run"
        style="margin-top:10px;padding:8px 16px;cursor:pointer;">
        ▶ コードを実行
      </button>

      <p id="status" aria-live="polite"></p>
      <h4>実行結果</h4>

      <pre id="output"
        style="box-sizing:border-box;background:#f0f2f6;color:#222;
        padding:12px;height:300px;max-height:300px;
        overflow-y:auto;overflow-x:auto;white-space:pre-wrap;
        overflow-wrap:anywhere;border:1px solid #ccc;
        border-radius:6px;margin:0;"></pre>
    </div>

    <script>
      const button = document.getElementById("run");
      const output = document.getElementById("output");
      const status = document.getElementById("status");
      let pyodide = null;

      button.addEventListener("click", async () => {
        button.disabled = true;
        output.textContent = "";
        status.textContent =
          "Pythonを準備しています。初回は少し時間がかかります。";

        try {
          if (!pyodide) {
            if (!window.loadPyodide) {
              await new Promise((resolve, reject) => {
                const script = document.createElement("script");
                script.src =
                  "https://cdn.jsdelivr.net/pyodide/v0.27.7/full/pyodide.js";
                script.onload = resolve;
                script.onerror = () => reject(
                  new Error("Python実行環境を読み込めませんでした。")
                );
                document.head.appendChild(script);
              });
            }

            pyodide = await loadPyodide();
          }

          let captured = [];

          pyodide.setStdout({
            batched: (text) => captured.push(text)
          });

          pyodide.setStderr({
            batched: (text) => captured.push(text)
          });

          await pyodide.runPythonAsync(
            document.getElementById("code").value
          );

          output.textContent = captured.join("\n") ||
            "実行完了！（表示する結果はありません）";

          status.textContent = "実行が終わりました。";

        } catch (error) {
          output.textContent = String(error);
          status.textContent = "実行中にエラーが発生しました。";

        } finally {
          button.disabled = false;
        }
      });
    </script>
    """,
    height=650,
    scrolling=False,
)

# =====================================
# 学習モード
# =====================================

mode = st.radio(
    "学習モードを選んでください",
    [
        "Pythonを質問する",
        "ヒントをもらう",
        "おみくじゲームを作る",
        "じゃんけんゲームを作る",
        "作ったゲームを改良する"
    ]
)

# =====================================
# モード別の指示
# =====================================

instructions = {
    "Pythonを質問する": """
Pythonについて、初心者にも分かる日本語で説明してください。
短いコード例を入れてください。
一度に説明しすぎないでください。
""",

    "ヒントをもらう": """
すぐに答えを全部教えず、まず短いヒントを1つ出してください。
学習者が「コードを見せて」と言ったら、
必要な部分のコードを示してください。
""",

    "おみくじゲームを作る": """
おみくじゲームを小さなステップに分けて教えてください。
print、random、変数を段階的に使います。
完成コードを最初から全部見せず、
学習者自身に書いてもらってください。
1回の回答で次にやる作業を1つだけ説明してください。
コードが送られたら確認し、直す点を説明してください。
ゲームが完成したら、簡単な改造アイデアを1つ紹介してください。
""",

    "じゃんけんゲームを作る": """
じゃんけんゲームを小さなステップに分けて教えてください。
input、random、ifを段階的に使います。
完成コードを最初から全部見せず、
学習者自身に書いてもらってください。
1回の回答で次にやる作業を1つだけ説明してください。
コードが送られたら確認し、直す点を説明してください。
ゲームが完成したら、簡単な改造アイデアを1つ紹介してください。
""",

    "作ったゲームを改良する": """
あなたは、小学生にも分かりやすく教える
Pythonゲーム改良アシスタントです。

特におみくじゲームとじゃんけんゲームの改良を得意としています。

【最初の対応】
まだコードが送られていない場合は、
改良したいゲームの種類と追加したい機能を聞いてください。
例：
・おみくじゲームにラッキーカラーを追加したい
・じゃんけんゲームで勝った回数を記録したい
・ゲームの表示をもっと楽しくしたい

【改良のルール】
1. 送られたコードをよく確認する
2. 元のゲームの良いところを残す
3. 希望された部分を中心に改良する
4. 初心者にも分かる言葉で変更点を説明する
5. 必要に応じて、変更したコード全体を提示する
6. エラーがある場合は原因と直し方を説明する
7. 希望されていない機能を勝手に追加しない
8. 一度に説明しすぎない

【おみくじゲームの改良例】
・大吉、中吉、小吉、凶などの結果を追加
・ラッキーカラーやラッキーアイテムを追加
・結果に合わせたメッセージを表示
・絵文字を使って見た目を楽しくする

【じゃんけんゲームの改良例】
・勝ち、負け、あいこの回数を記録
・3回勝負にする
・連勝記録を表示
・結果に合わせたメッセージを表示

コードがまだない場合は、先にコードを貼ってもらってください。
ただし、学習者が新しく作りたいと希望した場合は、
必要なコードを段階的に教えてください。
APIキーなどの秘密情報は求めないでください。
"""
}

# =====================================
# 会話履歴の初期化
# =====================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "previous_mode" not in st.session_state:
    st.session_state.previous_mode = mode

if st.session_state.previous_mode != mode:
    st.session_state.messages = []
    st.session_state.previous_mode = mode

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None

# =====================================
# 会話履歴を表示
# =====================================

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message.get("is_code", False):
            st.code(message["content"], language="python")
        else:
            st.markdown(message["content"])

# =====================================
# 質問を処理する関数
# =====================================

def process_question(question):
    is_code = "\n" in question

    st.session_state.messages.append({
        "role": "user",
        "content": question,
        "is_code": is_code
    })

    with st.chat_message("user"):
        if is_code:
            st.code(question, language="python")
        else:
            st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("AIが考えています..."):
            try:
                prompt = f"""
あなたは小学生高学年から中学生向けの
Pythonプログラミング学習支援チャットボットです。

【学習モード】
{mode}

【このモードの指示】
{instructions[mode]}

【共通ルール】
・簡単で分かりやすい日本語を使う
・学習者が自分で考えるのを助ける
・送られたPythonコードを確認する
・間違いがあれば理由と直し方を説明する
・日本語で回答する
・APIキーなどの秘密情報を求めない

【これまでの会話】
"""
                for message in st.session_state.messages[-8:]:
                    speaker = (
                        "学習者"
                        if message["role"] == "user"
                        else "AI"
                    )
                    prompt += (
                        f"\n{speaker}：\n{message['content']}\n"
                    )

                response = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        thinking_config=types.ThinkingConfig(
                            thinking_level="minimal"
                        )
                    )
                )

                answer = response.text or (
                    "回答が返ってきませんでした。もう一度試してください。"
                )

            except Exception as e:
                error = str(e)

                if "429" in error or "RESOURCE_EXHAUSTED" in error:
                    answer = (
                        "⚠️ APIの利用上限に達している可能性があります。"
                        "時間をおいてから、もう一度試してください。"
                    )
                elif "503" in error or "UNAVAILABLE" in error:
                    answer = (
                        "⚠️ Geminiが混雑しています。"
                        "少し時間をおいてから試してください。"
                    )
                elif "504" in error or "DEADLINE_EXCEEDED" in error:
                    answer = (
                        "⚠️ 回答に時間がかかりすぎました。"
                        "もう一度試してください。"
                    )
                else:
                    answer = (
                        "⚠️ 通信中にエラーが発生しました。"
                        "設定や実行ログを確認してください。"
                    )
                    print("Gemini API error:", error)

        st.markdown(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "is_code": False
    })

# =====================================
# 保留中の質問を処理
# =====================================

if st.session_state.pending_question is not None:
    question = st.session_state.pending_question
    st.session_state.pending_question = None
    process_question(question)

# =====================================
# 質問入力欄
# =====================================

with st.form("chat_form", clear_on_submit=True):
    question = st.text_area(
        "質問やPythonコードを入力してください",
        height=150,
        placeholder=(
            "例：\n"
            "おみくじゲームにラッキーカラーを追加したい\n\n"
            "または、改良したいゲームのコードを貼り付けてください"
        )
    )

    submitted = st.form_submit_button("送信")

if submitted and question.strip():
    st.session_state.pending_question = question.strip()
    st.rerun()

# =====================================
# 会話リセット
# =====================================

st.divider()

if st.button("🗑️ 会話をリセット"):
    st.session_state.messages = []
    st.session_state.pending_question = None
    st.rerun()
