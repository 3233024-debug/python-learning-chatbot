import os
import streamlit as st
import streamlit.components.v1 as components
from google import genai
from google.genai import types

# =========================================
# 🌈 ページ設定
# =========================================

st.set_page_config(
    page_title="わくわく！Pythonラボ",
    page_icon="🐼",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =========================================
# 🎨 デザイン
# =========================================

st.markdown("""
<style>
.stApp {
    background: linear-gradient(
        135deg, #fff5fb 0%, #f0f7ff 50%, #f2fff7 100%
    );
}

.block-container {
    max-width: 1100px;
    padding: 1.5rem 1.5rem 3rem 1.5rem;
}

h1, h2, h3 {
    color: #6047ad !important;
}

p, li {
    color: #45445c;
    line-height: 1.8;
}

.stButton > button,
.stFormSubmitButton > button {
    border: 0;
    border-radius: 14px;
    min-height: 45px;
    background: linear-gradient(100deg, #8b6ce8, #6798f5);
    color: white;
    font-weight: 800;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    color: white;
    border: 0;
    filter: brightness(1.05);
}

.stTextArea textarea {
    border: 2px solid #e1d9ff;
    border-radius: 14px;
    background: white;
    color: #303047;
    line-height: 1.8;
}

div[role="radiogroup"] {
    background: #ffffffc9;
    border: 1px solid #e8e0ff;
    border-radius: 20px;
    padding: 14px 16px;
    gap: 12px;
}

div[role="radiogroup"] label {
    color: #4c4770;
    font-weight: 650;
}

[data-testid="stChatMessage"] {
    background: #ffffffc9;
    border: 1px solid #ebe5ff;
    border-radius: 18px;
    padding: 1rem;
    margin-bottom: 1rem;
}

[data-testid="stForm"] {
    background: #ffffffbd;
    border: 1px solid #e7dfff;
    border-radius: 18px;
    padding: 16px;
}

@media (max-width: 700px) {
    .block-container {
        padding: 1rem 1rem 2rem 1rem;
    }
}
</style>
""", unsafe_allow_html=True)

# =========================================
# 🐼 ヘッダー
# =========================================

st.markdown("""
<div style="
    background: linear-gradient(120deg, #e8ddff, #dff1ff, #dcffed);
    border: 2px solid white;
    border-radius: 24px;
    padding: 28px 24px;
    text-align: center;
    margin-bottom: 20px;
">
    <div style="font-size: 52px;">🐼 🐸 🐰</div>
    <div style="
        font-size: 30px;
        font-weight: 900;
        color: #6047ad;
        margin: 8px 0;
    ">
        わくわく！Pythonラボ
    </div>
    <div style="font-size: 16px; color: #514c75; line-height: 1.9;">
        🎮 ゲームを作ろう！<br>
        💡 アイデアを形にしよう！<br>
        🌟 AI先生と楽しくプログラミング！
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================
# 🔑 APIキー確認
# =========================================

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    try:
        api_key = st.secrets.get("GEMINI_API_KEY")
    except Exception:
        api_key = None

if not api_key:
    st.error(
        "🔑 APIキーが設定されていません。"
        "Streamlit CloudのSecrets設定を確認してください。"
    )
    st.stop()

# =========================================
# 🤖 Geminiクライアント
# =========================================

@st.cache_resource
def get_client(key):
    return genai.Client(
        api_key=key,
        http_options={"timeout": 60000},
    )

client = get_client(api_key)

# =========================================
# 🧪 Pythonコード実行エリア
# =========================================

st.markdown("""
<div style="
    background: white;
    border: 2px solid #dcd4ff;
    border-radius: 20px;
    padding: 18px 20px;
    margin: 12px 0;
">
    <div style="font-size: 24px; font-weight: 850; color: #6047ad;">
        🧪 Pythonコード実験室
    </div>
    <div style="color: #66617f; line-height: 1.8;">
        自分のコードを書いて、実行してみよう！<br>
        失敗しても大丈夫。何度でも挑戦できるよ！
    </div>
</div>
""", unsafe_allow_html=True)

components.html(
    r"""
    <div style="
        font-family: Arial, sans-serif;
        background: white;
        border: 2px solid #e4dcff;
        border-radius: 18px;
        padding: 16px;
        box-sizing: border-box;
    ">
        <div style="
            color: #6047ad;
            font-size: 17px;
            font-weight: bold;
            margin-bottom: 10px;
        ">
            💻 コード入力
        </div>

        <textarea id="code" spellcheck="false" style="
            box-sizing: border-box;
            width: 100%;
            height: 220px;
            resize: vertical;
            font-family: Consolas, monospace;
            font-size: 14px;
            line-height: 1.7;
            padding: 14px;
            border: 2px solid #ddd5ff;
            border-radius: 12px;
            background: #faf9ff;
            color: #302d46;
        ">print("こんにちは！")
print("🐼 Pythonラボへようこそ！")

for i in range(1, 6):
    print("⭐ チャレンジ", i)

print("🎉 実行できたね！")</textarea>

        <button id="run" style="
            margin-top: 12px;
            width: 100%;
            padding: 13px;
            border: 0;
            border-radius: 12px;
            background: linear-gradient(100deg, #8b6ce8, #6798f5);
            color: white;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
        ">
            ▶ コードを実行する！
        </button>

        <div id="status" aria-live="polite" style="
            margin: 12px 0;
            color: #6353a0;
            font-size: 14px;
            line-height: 1.7;
        ">
            🌟 準備OK！実行ボタンを押してみよう。
        </div>

        <div style="
            color: #23836b;
            font-size: 17px;
            font-weight: bold;
            margin: 12px 0 8px;
        ">
            📺 実行結果
        </div>

        <pre id="output" style="
            box-sizing: border-box;
            background: #24243a;
            color: #e5e8ff;
            padding: 16px;
            height: 300px;
            overflow: auto;
            white-space: pre-wrap;
            overflow-wrap: anywhere;
            border: 2px solid #393958;
            border-radius: 12px;
            margin: 0;
            font-family: Consolas, monospace;
            font-size: 14px;
            line-height: 1.8;
        ">✨ ここに実行結果が表示されるよ！</pre>

        <div style="
            color: #77718e;
            font-size: 12px;
            margin-top: 10px;
            line-height: 1.7;
        ">
            💡 長い結果は黒い枠の中でスクロールできるよ。<br>
            ※ input()を使う対話型プログラムは、この実行欄ではそのまま動かない場合があります。
        </div>
    </div>

    <script>
    const button = document.getElementById("run");
    const output = document.getElementById("output");
    const status = document.getElementById("status");
    let pyodide = null;

    button.addEventListener("click", async () => {
        button.disabled = true;
        output.textContent = "";
        status.textContent = "⏳ Pythonを準備しています...";

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

            const captured = [];

            pyodide.setStdout({
                batched: (text) => captured.push(text)
            });

            pyodide.setStderr({
                batched: (text) => captured.push(text)
            });

            const code = document.getElementById("code").value;

            await pyodide.runPythonAsync(code);

            output.textContent = captured.join("\n") ||
                "🎉 実行完了！表示する結果はありません。";

            status.textContent = "🎉 実行成功！よくできました！";

        } catch (error) {
            output.textContent = String(error);
            status.textContent =
                "💦 エラーが発生しました。コードを確認してみよう。";

        } finally {
            button.disabled = false;
        }
    });
    </script>
    """,
    height=850,
    scrolling=False,
)

# =========================================
# 🎮 学習モード選択
# =========================================

st.divider()

st.markdown("""
<div style="
    text-align: center;
    background: linear-gradient(120deg, #fff0fa, #f0edff);
    border-radius: 18px;
    padding: 18px;
    margin-bottom: 14px;
">
    <div style="font-size: 28px;">🎮 🌈 💡</div>
    <div style="
        color: #6047ad;
        font-size: 24px;
        font-weight: 900;
    ">
        どの冒険に出発する？
    </div>
    <div style="color: #68617f; line-height: 1.8;">
        好きなモードを選んで、AI先生と学ぼう！
    </div>
</div>
""", unsafe_allow_html=True)

mode_options = [
    "🐍 Pythonを質問する",
    "💡 ヒントをもらう",
    "🔮 おみくじゲームを作る",
    "✊ じゃんけんゲームを作る",
    "🛠️ 作ったゲームを改良する",
]

mode_map = {
    "🐍 Pythonを質問する": "Pythonを質問する",
    "💡 ヒントをもらう": "ヒントをもらう",
    "🔮 おみくじゲームを作る": "おみくじゲームを作る",
    "✊ じゃんけんゲームを作る": "じゃんけんゲームを作る",
    "🛠️ 作ったゲームを改良する": "作ったゲームを改良する",
}

selected_mode = st.radio(
    "学習モード",
    mode_options,
    label_visibility="collapsed",
)

mode = mode_map[selected_mode]

mode_descriptions = {
    "Pythonを質問する": "わからないことをAI先生に聞いてみよう！",
    "ヒントをもらう": "答えを考えるためのヒントをもらおう！",
    "おみくじゲームを作る": "運だめしゲームを作ってみよう！",
    "じゃんけんゲームを作る": "コンピューターと勝負しよう！",
    "作ったゲームを改良する": "今あるゲームに新しい機能を追加しよう！",
}

st.info(f"🌟 {mode_descriptions[mode]}")

# =========================================
# 📚 モード別の指示
# =========================================

instructions = {
    "Pythonを質問する": """
Pythonについて、初心者にも分かる日本語で説明してください。
短いコード例を入れてください。
一度に説明しすぎず、必要なら例を使ってください。
""",

    "ヒントをもらう": """
すぐに答えを全部教えず、まず短いヒントを1つ出してください。
学習者が「コードを見せて」と言ったら、
必要な部分のコードを示してください。
""",

    "おみくじゲームを作る": """
おみくじゲームを小さなステップに分けて教えてください。
print、random、変数、リスト、ifを段階的に使います。
最初から完成コードを全部見せず、学習者自身にコードを書いてもらいます。
1回の回答では次の作業を1つだけ説明してください。
「ヒント」と言われたら短いヒントを1つ出してください。
「コードを見せて」と言われたら必要な部分だけ見せてください。
コードが送られたら確認し、直す点を説明してください。
完成したら「ゲーム完成です！」と伝え、改造アイデアを1つ紹介してください。
""",

    "じゃんけんゲームを作る": """
じゃんけんゲームを小さなステップに分けて教えてください。
print、random、変数、リスト、ifを段階的に使います。
最初から完成コードを全部見せず、学習者自身にコードを書いてもらいます。
1回の回答では次の作業を1つだけ説明してください。
「ヒント」と言われたら短いヒントを1つ出してください。
「コードを見せて」と言われたら必要な部分だけ見せてください。
コードが送られたら確認し、直す点を説明してください。
完成したら「ゲーム完成です！」と伝え、改造アイデアを1つ紹介してください。
""",

    "作ったゲームを改良する": """
あなたは、小学生にも分かりやすく教えるPythonゲーム改良アシスタントです。

特におみくじゲームとじゃんけんゲームを改良します。
最初に、改良したいゲームと追加したい機能を確認してください。
コードがまだない場合は、改良したいゲームのコードを貼り付けてもらってください。

おみくじゲームの改良例：
・大吉、中吉、小吉、凶などを追加する
・ラッキーカラーやラッキーアイテムを追加する
・結果に合わせたメッセージを表示する

じゃんけんゲームの改良例：
・勝ち、負け、あいこの回数を記録する
・3回勝負にする
・連勝記録を表示する

送られたコードを確認し、元のゲームの良いところを残してください。
希望された部分を中心に改良し、変更点を初心者にも分かる言葉で説明してください。
必要に応じて実行できるコード全体を示してください。
""",
}

# =========================================
# 💬 会話履歴を準備
# =========================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "previous_mode" not in st.session_state:
    st.session_state.previous_mode = mode

if st.session_state.previous_mode != mode:
    st.session_state.messages = []
    st.session_state.previous_mode = mode

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None

# =========================================
# 💬 会話履歴を表示
# =========================================

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message.get("is_code", False):
            st.code(message["content"], language="python")
        else:
            st.markdown(message["content"])

# =========================================
# 🤖 質問を処理
# =========================================

def process_question(question):
    is_code = "\n" in question

    st.session_state.messages.append({
        "role": "user",
        "content": question,
        "is_code": is_code,
    })

    with st.chat_message("user"):
        if is_code:
            st.code(question, language="python")
        else:
            st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("🐣 AI先生が考えています..."):
            try:
                prompt = f"""
あなたは小学生高学年から中学生向けの
Pythonプログラミング学習支援チャットボットです。

【学習モード】
{mode}

【このモードの指示】
{instructions[mode]}

【共通ルール】
・やさしく、分かりやすい日本語を使う
・読みやすいように適度に改行する
・長い文章は箇条書きにする
・必要に応じて絵文字を使う
・一度に説明しすぎない
・学習者が自分で考えるのを助ける
・送られたPythonコードを確認する
・間違いがあれば理由と直し方を説明する
・APIキーなどの秘密情報を求めない

【これまでの会話】
"""

                for message in st.session_state.messages[-8:]:
                    speaker = (
                        "学習者"
                        if message["role"] == "user"
                        else "AI先生"
                    )
                    prompt += (
                        f"\n{speaker}：\n"
                        f"{message['content']}\n"
                    )

                response = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        thinking_config=types.ThinkingConfig(
                            thinking_level="minimal"
                        )
                    ),
                )

                answer = response.text or (
                    "回答が返ってきませんでした。もう一度試してね！"
                )

            except Exception as e:
                error = str(e)

                if "429" in error or "RESOURCE_EXHAUSTED" in error:
                    answer = (
                        "⏳ APIの利用上限に達している可能性があります。\n\n"
                        "少し時間をおいてから、もう一度試してね！"
                    )
                elif "503" in error or "UNAVAILABLE" in error:
                    answer = (
                        "🚦 AI先生が混雑しているみたい。\n\n"
                        "少し待ってから、もう一度試してね！"
                    )
                elif "504" in error or "DEADLINE_EXCEEDED" in error:
                    answer = (
                        "⌛ 回答に時間がかかりすぎました。\n\n"
                        "もう一度試してね！"
                    )
                else:
                    answer = (
                        "💦 通信中にエラーが発生しました。\n\n"
                        "しばらくしてからもう一度試してね。"
                    )
                    print("Gemini API error:", error)

        st.markdown(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "is_code": False,
    })

# =========================================
# 📝 入力欄
# Python質問モードのときだけ表示
# =========================================

st.divider()

st.markdown("## 💌 AI先生に聞いてみよう！")

if mode == "Pythonを質問する":
    st.write(
        "分からない問題やPythonの疑問を入力してね。"
        "コードについての質問もできるよ！"
    )
elif mode == "ヒントをもらう":
    st.write("問題や書いているコードを入力して、ヒントをもらおう！")
elif mode == "おみくじゲームを作る":
    st.write("おみくじゲームを作ろう！最初の質問やコードを入力してね。")
elif mode == "じゃんけんゲームを作る":
    st.write("じゃんけんゲームを作ろう！分からないところを入力してね。")
else:
    st.write("改良したいゲームのコードや、追加したい機能を入力してね。")

with st.form("chat_form", clear_on_submit=True):
    question = st.text_area(
        "📝 メッセージを入力",
        height=120,
        placeholder=(
            "例：Pythonのif文の使い方を教えて！\n"
            "例：じゃんけんゲームを作りたい！"
        ),
    )

    submitted = st.form_submit_button(
        "🚀 送信する",
        use_container_width=True,
    )

if submitted:
    if question.strip():
        st.session_state.pending_question = question.strip()
        st.rerun()
    else:
        st.warning("メッセージを入力してから送信してね！")

# =========================================
# 🔄 送信された質問を処理
# =========================================

if st.session_state.pending_question:
    pending = st.session_state.pending_question
    st.session_state.pending_question = None
    process_question(pending)

# =========================================
# 🧹 会話リセット
# =========================================

st.divider()

if st.button("🧹 このモードの会話をリセット"):
    st.session_state.messages = []
    st.session_state.pending_question = None
    st.rerun()

# =========================================
# 🌟 フッター
# =========================================

st.markdown("""
<div style="
    text-align: center;
    color: #77718e;
    padding: 20px 8px;
    line-height: 1.9;
">
    🐼 🐸 🐰<br>
    <b>わくわく！Pythonラボ</b><br>
    少しずつ挑戦して、楽しくプログラミングを学ぼう！ 🌈
</div>
""", unsafe_allow_html=True)
