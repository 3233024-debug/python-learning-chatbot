
import os
import streamlit as st
import streamlit.components.v1 as components
from google import genai
from google.genai import types

# =========================================
# ページ設定
# =========================================

st.set_page_config(
    page_title="わくわく！Pythonラボ",
    page_icon="🐼",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =========================================
# デザイン
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
</style>
""", unsafe_allow_html=True)

# =========================================
# ヘッダー
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
# APIキー確認
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
# Geminiクライアント
# =========================================

@st.cache_resource
def get_client(key):
    return genai.Client(
        api_key=key,
        http_options={"timeout": 60000},
    )

client = get_client(api_key)

# =========================================
# Pythonコード実験室
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
    font-family:Arial,sans-serif;
    background:white;
    border:2px solid #e4dcff;
    border-radius:18px;
    padding:16px;
">

    <h3 style="color:#6047ad;">💻 コード入力</h3>

    <textarea id="code" spellcheck="false" style="
        box-sizing:border-box;
        width:100%;
        height:240px;
        resize:vertical;
        font-family:Consolas,monospace;
        font-size:14px;
        line-height:1.7;
        padding:14px;
        border:2px solid #ddd5ff;
        border-radius:12px;
        background:#faf9ff;
        color:#302d46;
    ">name = input("名前を入力してください：")
print("こんにちは、" + name + "さん！")

age = input("年齢を入力してください：")
print("あなたは", age, "歳なんだね！")</textarea>

    <button id="prepare" style="
        margin-top:12px;
        width:100%;
        padding:13px;
        border:0;
        border-radius:12px;
        background:linear-gradient(100deg,#8b6ce8,#6798f5);
        color:white;
        font-size:16px;
        font-weight:bold;
        cursor:pointer;
    ">
        ▶ コードを実行する！
    </button>

    <div id="input-area" style="
        display:none;
        background:#f4f0ff;
        border:2px solid #cfc2ff;
        border-radius:14px;
        padding:15px;
        margin-top:15px;
    ">
        <h3 style="color:#6047ad;">⌨️ Pythonの入力コーナー</h3>
        <div id="input-fields"></div>
        <button id="execute" style="
            margin-top:12px;
            width:100%;
            padding:13px;
            border:0;
            border-radius:12px;
            background:#23836b;
            color:white;
            font-size:16px;
            font-weight:bold;
            cursor:pointer;
        ">
            ✅ 入力内容で実行！
        </button>
    </div>

    <div id="game-area" style="
        display:none;
        margin-top:18px;
        padding:16px;
        background:#f4f0ff;
        border:2px solid #cfc2ff;
        border-radius:16px;
    ">
        <h2 id="game-title" style="
            color:#6047ad;
            text-align:center;
        "></h2>

        <div id="game-result" style="
            text-align:center;
            font-size:22px;
            font-weight:bold;
            color:#6047ad;
            margin:18px 0;
        "></div>

        <div id="janken-buttons" style="
            display:none;
            gap:8px;
            justify-content:center;
            flex-wrap:wrap;
        ">
            <button class="hand" data-hand="グー">✊ グー</button>
            <button class="hand" data-hand="チョキ">✌️ チョキ</button>
            <button class="hand" data-hand="パー">✋ パー</button>
        </div>

        <div id="score-area" style="
            display:none;
            gap:8px;
            margin-top:18px;
            text-align:center;
        ">
            <div class="score">
                🏆 勝ち<br><b id="wins">0</b>
            </div>
            <div class="score">
                💦 負け<br><b id="losses">0</b>
            </div>
            <div class="score">
                🤝 あいこ<br><b id="draws">0</b>
            </div>
        </div>

        <button id="omikuji-button" style="
            display:none;
            width:100%;
            padding:14px;
            margin-top:12px;
            border:0;
            border-radius:12px;
            background:#8b6ce8;
            color:white;
            font-size:17px;
            font-weight:bold;
            cursor:pointer;
        ">
            🔄 もう一度おみくじを引く！
        </button>

        <button id="reset-button" style="
            display:none;
            width:100%;
            padding:12px;
            margin-top:12px;
            border:0;
            border-radius:12px;
            background:#77718e;
            color:white;
            font-weight:bold;
            cursor:pointer;
        ">
            🔄 成績をリセット
        </button>
    </div>

    <div id="status" style="
        margin:12px 0;
        color:#6353a0;
        font-size:14px;
        line-height:1.7;
    ">
        🌟 準備OK！実行ボタンを押してみよう。
    </div>

    <h3 style="color:#23836b;">📺 実行結果</h3>

    <pre id="output" style="
        box-sizing:border-box;
        background:#24243a;
        color:#e5e8ff;
        padding:16px;
        height:230px;
        overflow:auto;
        white-space:pre-wrap;
        overflow-wrap:anywhere;
        border:2px solid #393958;
        border-radius:12px;
        margin:0;
        font-family:Consolas,monospace;
        font-size:14px;
        line-height:1.8;
    ">✨ ここに実行結果が表示されるよ！</pre>

    <div style="
        color:#77718e;
        font-size:12px;
        margin-top:10px;
        line-height:1.7;
    ">
        💡 input()を使うと入力欄が表示されるよ！<br>
        ゲーム用コードでは、サイトのボタンから操作できるよ！
    </div>
</div>

<style>
.hand {
    padding:14px 18px;
    border:0;
    border-radius:12px;
    background:#8b6ce8;
    color:white;
    font-size:18px;
    font-weight:bold;
    cursor:pointer;
}
.score {
    flex:1;
    background:white;
    padding:12px;
    border-radius:12px;
    color:#6047ad;
    font-size:15px;
}
.score b {
    font-size:25px;
}
button:disabled {
    opacity:.5;
    cursor:not-allowed;
}
</style>

<script>
const codeArea = document.getElementById("code");
const prepareButton = document.getElementById("prepare");
const executeButton = document.getElementById("execute");
const inputArea = document.getElementById("input-area");
const inputFields = document.getElementById("input-fields");
const gameArea = document.getElementById("game-area");
const gameResult = document.getElementById("game-result");
const output = document.getElementById("output");
const status = document.getElementById("status");

let pyodide = null;
let currentCode = "";
let inputCount = 0;
let gameType = "";
let gameGlobals = null;

function countInputs(code) {
    const matches = code.match(/\binput\s*\(/g);
    return matches ? matches.length : 0;
}

async function preparePyodide() {
    if (!pyodide) {
        status.textContent = "⏳ Pythonを準備しています...";

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
}

function makeInputFields(count) {
    inputFields.innerHTML = "";

    for (let i = 0; i < count; i++) {
        const wrapper = document.createElement("div");
        wrapper.style.marginBottom = "12px";

        const label = document.createElement("label");
        label.textContent = `🐼 ${i + 1}回目の入力`;
        label.style.display = "block";
        label.style.fontWeight = "bold";
        label.style.color = "#6047ad";
        label.style.marginBottom = "6px";

        const field = document.createElement("input");
        field.type = "text";
        field.id = `python-input-${i}`;
        field.placeholder = `${i + 1}回目の答えを入力してね！`;
        field.style.cssText =
            "width:100%;box-sizing:border-box;padding:12px;border:2px solid #ddd5ff;border-radius:10px;";

        wrapper.appendChild(label);
        wrapper.appendChild(field);
        inputFields.appendChild(wrapper);
    }

    inputArea.style.display = count > 0 ? "block" : "none";
}

function setScore(scoreProxy) {
    const score = scoreProxy.toJs({
        dict_converter: Object.fromEntries
    });

    document.getElementById("wins").textContent = score.wins;
    document.getElementById("losses").textContent = score.losses;
    document.getElementById("draws").textContent = score.draws;

    scoreProxy.destroy();
}

function showError(error) {
    const errorText = String(error);
    let explanation =
        "エラーの原因を特定できませんでした。エラー文を確認してみよう！";

    if (errorText.includes("SyntaxError")) {
        explanation =
            "📝 文法エラーだよ！カッコや引用符、コロンを確認してみよう。";
    } else if (errorText.includes("NameError")) {
        explanation =
            "🔍 名前エラーだよ！変数名や関数名のスペルを確認してみよう。";
    } else if (errorText.includes("TypeError")) {
        explanation =
            "🧩 型エラーだよ！数字と文字列などの使い方を確認してみよう。";
    } else if (errorText.includes("IndentationError")) {
        explanation =
            "📐 インデントエラーだよ！行の先頭の空白を確認してみよう。";
    } else if (errorText.includes("IndexError")) {
        explanation =
            "📦 リストの範囲エラーだよ！存在しない番号を使っていないか確認しよう。";
    } else if (errorText.includes("ZeroDivisionError")) {
        explanation =
            "➗ 0で割ろうとしているよ！割り算の右側を確認しよう。";
    } else if (errorText.includes("EOFError")) {
        explanation =
            "⌨️ 入力が途中で終了したよ！input()の入力を確認しよう。";
    }

    output.textContent =
        "【エラーの内容】\n" + errorText +
        "\n\n【💡 AI先生からのヒント】\n" + explanation;

    status.textContent =
        "💦 エラーを見つけたよ！ヒントを参考に直してみよう。";
}

async function callGameFunction(functionName, argument = null) {
    if (!gameGlobals) {
        throw new Error("ゲームが読み込まれていません。");
    }

    pyodide.globals.set("site_game_globals", gameGlobals);

    if (argument === null) {
        return await pyodide.runPythonAsync(
            `site_game_globals[${JSON.stringify(functionName)}]()`
        );
    }

    pyodide.globals.set("site_game_argument", argument);

    return await pyodide.runPythonAsync(
        `site_game_globals[${JSON.stringify(functionName)}](site_game_argument)`
    );
}

async function startGame() {
    gameArea.style.display = "block";
    inputArea.style.display = "none";
    gameResult.textContent = "";

    if (gameType === "janken") {
        document.getElementById("game-title").textContent =
            "✊ じゃんけんゲーム！";

        document.getElementById("janken-buttons").style.display = "flex";
        document.getElementById("score-area").style.display = "flex";
        document.getElementById("reset-button").style.display = "block";
        document.getElementById("omikuji-button").style.display = "none";

        const score = await callGameFunction("get_score");
        setScore(score);
    }

    if (gameType === "omikuji") {
        document.getElementById("game-title").textContent =
            "🔮 おみくじゲーム！";

        document.getElementById("janken-buttons").style.display = "none";
        document.getElementById("score-area").style.display = "none";
        document.getElementById("reset-button").style.display = "none";
        document.getElementById("omikuji-button").style.display = "block";

        await drawOmikuji();
    }
}

async function drawOmikuji() {
    try {
        const result = await callGameFunction("draw_omikuji");
        gameResult.textContent = String(result);
        status.textContent = "🌟 おみくじを引いたよ！";
    } catch (error) {
        showError(error);
    }
}

prepareButton.addEventListener("click", async () => {
    currentCode = codeArea.value;
    inputCount = countInputs(currentCode);
    gameType = "";
    gameGlobals = null;

    output.textContent = "";
    gameArea.style.display = "none";
    inputArea.style.display = "none";

    prepareButton.disabled = true;

    try {
        await preparePyodide();

        // GAME_TYPEを宣言しているか確認
        const gameMatch = currentCode.match(
            /^\s*GAME_TYPE\s*=\s*["'](janken|omikuji)["']/m
        );

        if (gameMatch) {
            gameType = gameMatch[1];

            if (inputCount > 0) {
                throw new Error(
                    "ゲーム用コードではinput()を使わず、サイトのボタンを使ってね。"
                );
            }

            // ゲーム専用の名前空間を作る
            await pyodide.runPythonAsync(
                "game_globals = {}"
            );

            pyodide.globals.set("site_user_code", currentCode);

            await pyodide.runPythonAsync(
                "exec(compile(site_user_code, '<user code>', 'exec'), game_globals)"
            );

            gameGlobals = pyodide.globals.get("game_globals");

            await startGame();

            status.textContent = "🎮 ゲームの準備ができたよ！";

        } else if (inputCount > 0) {
            makeInputFields(inputCount);
            status.textContent =
                `✏️ ${inputCount}個の入力欄を用意したよ！答えを入力してね。`;

            document.getElementById("python-input-0").focus();

        } else {
            await runOrdinaryPython([]);
        }

    } catch (error) {
        showError(error);
    } finally {
        prepareButton.disabled = false;
    }
});

async function runOrdinaryPython(values) {
    output.textContent = "";
    status.textContent = "🐍 Pythonを実行しています...";

    try {
        const captured = [];

        pyodide.setStdout({
            batched: text => captured.push(text)
        });

        pyodide.setStderr({
            batched: text => captured.push(text)
        });

        let inputBuffer = [];

        for (const value of values) {
            inputBuffer.push(
                ...new TextEncoder().encode(value + "\n")
            );
        }

        pyodide.setStdin({
            stdin: () => {
                if (inputBuffer.length === 0) {
                    return null;
                }
                return inputBuffer.shift();
            },
            isatty: true
        });

        pyodide.globals.set("site_user_code", currentCode);

        await pyodide.runPythonAsync(
            "exec(compile(site_user_code, '<user code>', 'exec'), {})"
        );

        output.textContent = captured.join("\n") ||
            "🎉 実行完了！表示する結果はありません。";

        status.textContent = "🎉 実行成功！よくできました！";

    } catch (error) {
        showError(error);
    }
}

executeButton.addEventListener("click", async () => {
    const values = [];

    for (let i = 0; i < inputCount; i++) {
        const field = document.getElementById(`python-input-${i}`);

        if (!field.value.trim()) {
            status.textContent =
                `⚠️ ${i + 1}回目の入力欄に答えを入力してね！`;
            field.focus();
            return;
        }

        values.push(field.value);
    }

    executeButton.disabled = true;
    prepareButton.disabled = true;

    await runOrdinaryPython(values);

    executeButton.disabled = false;
    prepareButton.disabled = false;
});

// じゃんけんボタン
document.querySelectorAll(".hand").forEach(button => {
    button.addEventListener("click", async () => {
        button.disabled = true;

        try {
            const result = await callGameFunction(
                "play",
                button.dataset.hand
            );

            gameResult.textContent = String(result);

            const score = await callGameFunction("get_score");
            setScore(score);

            status.textContent = "🎉 もう一回挑戦してみよう！";

        } catch (error) {
            showError(error);
        } finally {
            button.disabled = false;
        }
    });
});

// おみくじをもう一度引く
document.getElementById("omikuji-button")
.addEventListener("click", drawOmikuji);

// 成績リセット
document.getElementById("reset-button")
.addEventListener("click", async () => {
    try {
        await callGameFunction("reset_score");

        const score = await callGameFunction("get_score");
        setScore(score);

        gameResult.textContent = "成績をリセットしたよ！";
        status.textContent = "🔄 成績が0になったよ！";

    } catch (error) {
        showError(error);
    }
});
</script>
""",
    height=1450,
    scrolling=True,
)

# =========================================
# 学習モード選択
# =========================================

st.markdown("""
<div style="
    text-align:center;
    background:linear-gradient(120deg,#fff0fa,#f0edff);
    border-radius:18px;
    padding:18px;
    margin:20px 0 14px 0;
">
    <div style="font-size:28px;">🎮 🌈 💡</div>
    <div style="color:#6047ad;font-size:24px;font-weight:900;">
        どの冒険に出発する？
    </div>
    <div style="color:#68617f;line-height:1.8;">
        好きなモードを選んで、AI先生と学ぼう！
    </div>
</div>
""", unsafe_allow_html=True)

mode_options = [
    "🐍 Pythonに質問する",
    "🔮 おみくじゲームを作る",
    "✊ じゃんけんゲームを作る",
    "🛠️ 作ったゲームを改良する",
]

mode_map = {
    "🐍 Pythonに質問する": "Pythonに質問する",
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
    "Pythonに質問する": "わからないことをAI先生に聞いてみよう！",
    "おみくじゲームを作る": "運だめしゲームを作ってみよう！",
    "じゃんけんゲームを作る": "コンピューターと勝負しよう！",
    "作ったゲームを改良する": "今あるゲームに新しい機能を追加しよう！",
}

st.markdown(f"""
<div style="
    background:#dff1ff;
    border-radius:12px;
    padding:18px 22px;
    margin:16px 0;
    color:#45445c;
    font-size:20px;
">
    🌟 {mode_descriptions[mode]}
</div>
""", unsafe_allow_html=True)

# =========================================
# モード別の指示
# =========================================

instructions = {
    "Pythonに質問する": """
Pythonについて、初心者にも分かる日本語で説明してください。
短いコード例を入れてください。
一度に説明しすぎず、必要なら例を使ってください。
""",

    "おみくじゲームを作る": """
おみくじゲームを小さなステップに分けて教えてください。
print、random、変数、リスト、ifを段階的に使います。

完成コードはサイトのゲーム画面に対応させます。
完成コードには必ず次の形式を使います。

GAME_TYPE = "omikuji"

def draw_omikuji():
    # おみくじの結果を作る
    # 結果の文字列をreturnする

サイトの「もう一度おみくじを引く！」ボタンから
draw_omikuji()が呼び出されます。

ゲーム用コードではinput()やwhile Trueを使わないでください。

最初から完成コードを全部見せず、学習者自身にコードを書いてもらいます。
1回の回答では次の作業を1つだけ説明してください。
「ヒント」と言われたら短いヒントを1つ出してください。
「コードを見せて」と言われたら必要な部分だけ見せてください。
コードが送られたら確認し、直す点を説明してください。
完成したら「ゲーム完成です！」と伝えてください。
""",

    "じゃんけんゲームを作る": """
じゃんけんゲームを小さなステップに分けて教えてください。
print、random、変数、リスト、ifを段階的に使います。

完成コードはサイトのゲーム画面に対応させます。
完成コードには必ず次の形式を使います。

GAME_TYPE = "janken"

wins = 0
losses = 0
draws = 0

def play(player):
    # playerにはグー・チョキ・パーが渡される
    # 勝敗を判定して回数を増やす
    # 結果の文字列をreturnする

def get_score():
    return {
        "wins": wins,
        "losses": losses,
        "draws": draws
    }

def reset_score():
    # wins、losses、drawsを0に戻す

play()はサイトのグー・チョキ・パーのボタンから呼び出されます。
input()やwhile Trueは使わないでください。

最初から完成コードを全部見せず、学習者自身にコードを書いてもらいます。
1回の回答では次の作業を1つだけ説明してください。
「ヒント」と言われたら短いヒントを1つ出してください。
「コードを見せて」と言われたら必要な部分だけ見せてください。
コードが送られたら確認し、直す点を説明してください。
完成したら「ゲーム完成です！」と伝えてください。
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

サイト対応のゲームコードでは、
おみくじはGAME_TYPE = "omikuji"とdraw_omikuji()を使います。
じゃんけんはGAME_TYPE = "janken"とplay()、get_score()、reset_score()を使います。
ゲーム用コードではinput()やwhile Trueを使いません。

送られたコードを確認し、元のゲームの良いところを残してください。
希望された部分を中心に改良し、変更点を初心者にも分かる言葉で説明してください。
必要に応じて実行できるコード全体を示してください。
""",
}

# =========================================
# 会話履歴
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
# 質問を処理する関数
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
# 過去の会話を表示
# =========================================

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message.get("is_code", False):
            st.code(message["content"], language="python")
        else:
            st.markdown(message["content"])

# =========================================
# 送信された質問を処理
# =========================================

if st.session_state.pending_question:
    pending = st.session_state.pending_question
    st.session_state.pending_question = None
    process_question(pending)

# =========================================
# 質問入力欄
# =========================================

if mode == "Pythonに質問する":
    placeholder_text = "例：Pythonのif文の使い方を教えて！"
elif mode == "おみくじゲームを作る":
    placeholder_text = "例：次はおみくじの結果を表示したい！"
elif mode == "じゃんけんゲームを作る":
    placeholder_text = "例：コンピューターの手を決める方法を教えて！"
else:
    placeholder_text = "改良したいコードや追加したい機能を入力してね！"

with st.form("chat_form", clear_on_submit=True):
    question = st.text_area(
        "📝 質問・コードを入力",
        placeholder=placeholder_text,
        height=100,
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
        st.warning("質問を入力してね！")

# =========================================
# 会話リセット
# =========================================

if st.button("🧹 このモードの会話をリセット"):
    st.session_state.messages = []
    st.session_state.pending_question = None
    st.rerun()

# =========================================
# フッター
# =========================================

st.markdown("""
<div style="
    text-align:center;
    color:#77718e;
    padding:20px 8px;
    line-height:1.9;
">
    🐼 🐸 🐰<br>
    <b>わくわく！Pythonラボ</b><br>
</div>
""", unsafe_allow_html=True)
