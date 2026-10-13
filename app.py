
import os
import ast
import random
import io
import contextlib
import streamlit as st
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
    st.error("APIキーが設定されていません。")
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
# Pythonコード実行機能
# =====================================

st.divider()
st.header("🧪 Pythonコードを試す")
st.write("コードを書いて、実行結果を確認しよう！")

# 最初は空欄にする
if "code_editor" not in st.session_state:
    st.session_state.code_editor = ""

code = st.text_area(
    "Pythonコードを入力",
    key="code_editor",
    height=220,
    placeholder='例：print("こんにちは！")'
)

st.caption(
    "学習用の簡易実行機能です。"
    "公開環境向けの安全な実行環境ではありません。"
)

def run_learning_code(source):
    if len(source) > 5000:
        return "", "コードは5000文字以内にしてください。"

    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        return "", f"構文エラー: {e}"

    allowed_nodes = (
        ast.Module, ast.Expr, ast.Assign, ast.AugAssign,
        ast.Name, ast.Load, ast.Store, ast.Constant,
        ast.List, ast.Tuple, ast.Dict, ast.Set,
        ast.BinOp, ast.UnaryOp, ast.BoolOp, ast.Compare,
        ast.If, ast.For, ast.Break, ast.Continue, ast.Pass,
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
        ast.Mod, ast.Pow, ast.USub, ast.UAdd, ast.Not,
        ast.And, ast.Or, ast.Eq, ast.NotEq, ast.Lt,
        ast.LtE, ast.Gt, ast.GtE, ast.In, ast.NotIn,
        ast.Is, ast.IsNot, ast.Call, ast.keyword,
        ast.IfExp, ast.Subscript, ast.Slice,
        ast.ListComp, ast.comprehension,
        ast.JoinedStr, ast.FormattedValue,
        ast.Import, ast.alias, ast.Attribute
    )

    for node in ast.walk(tree):
        if not isinstance(node, allowed_nodes):
            return "", (
                f"{type(node).__name__} は"
                "この学習用実行機能では使えません。"
            )

        # import random のみ許可
        if isinstance(node, ast.Import):
            if (
                len(node.names) != 1
                or node.names[0].name != "random"
                or node.names[0].asname is not None
            ):
                return "", "使用できるimportは import random のみです。"

        # randomの指定された関数だけ許可
        if isinstance(node, ast.Attribute):
            if (
                not isinstance(node.value, ast.Name)
                or node.value.id != "random"
                or node.attr not in ("choice", "randint", "randrange")
            ):
                return "", "この属性の使用には対応していません。"

        # 使用できる関数を限定
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                if node.func.id not in (
                    "print", "range", "len", "str", "int",
                    "float", "bool", "list", "tuple", "dict",
                    "sum", "min", "max", "abs", "round",
                    "sorted", "enumerate", "zip"
                ):
                    return "", f"{node.func.id}() は使用できません。"

            elif isinstance(node.func, ast.Attribute):
                if (
                    not isinstance(node.func.value, ast.Name)
                    or node.func.value.id != "random"
                    or node.func.attr not in (
                        "choice", "randint", "randrange"
                    )
                ):
                    return "", "この関数の呼び出しには対応していません。"
            else:
                return "", "この関数の呼び出しには対応していません。"

        # rangeの繰り返し回数を制限
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id == "range":
                if not 1 <= len(node.args) <= 3:
                    return "", "range() の引数は1～3個にしてください。"

                if any(
                    not isinstance(arg, ast.Constant)
                    or type(arg.value) is not int
                    for arg in node.args
                ):
                    return "", "range() には整数を直接指定してください。"

                try:
                    values = [arg.value for arg in node.args]
                    if len(range(*values)) > 1000:
                        return "", "range() は最大1000回までです。"
                except (ValueError, OverflowError):
                    return "", "range() の指定を確認してください。"

    # importで読み込めるモジュールを限定
    def safe_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name == "random" and level == 0 and not fromlist:
            return random
        raise ImportError("このモジュールは使用できません。")

    safe_builtins = {
        "__import__": safe_import,
        "print": print,
        "range": range,
        "len": len,
        "str": str,
        "int": int,
        "float": float,
        "bool": bool,
        "list": list,
        "tuple": tuple,
        "dict": dict,
        "sum": sum,
        "min": min,
        "max": max,
        "abs": abs,
        "round": round,
        "sorted": sorted,
        "enumerate": enumerate,
        "zip": zip,
    }

    safe_globals = {
        "__builtins__": safe_builtins,
        "random": random,
    }

    output = io.StringIO()

    try:
        with contextlib.redirect_stdout(output):
            exec(compile(tree, "<学習コード>", "exec"), safe_globals)

        result = output.getvalue()
        if not result:
            result = "実行完了！（表示する結果はありません）"

        return result, None

    except Exception as e:
        return "", f"{type(e).__name__}: {e}"


# 実行ボタン
if st.button("▶ コードを実行", type="primary"):
    if not code.strip():
        st.warning("コードを入力してから実行してください。")
    else:
        result, error = run_learning_code(code)

        if error:
            st.error("実行中にエラーが発生しました")
            st.code(error)
        else:
            st.success("実行できました！")
            st.code(result, language="text")

        st.session_state.last_test_code = code
        st.session_state.last_test_error = error
        st.session_state.last_test_result = result

# エラーをAIに質問
if st.session_state.get("last_test_error"):
    if st.button("🤖 このエラーをAIに質問する"):
        st.session_state.pending_question = (
            "次のPythonコードのエラーについて、"
            "初心者にも分かるように原因と直し方を教えてください。\n\n"
            "コード:\n"
            + st.session_state.last_test_code
            + "\n\nエラー:\n"
            + st.session_state.last_test_error
        )
        st.rerun()

st.divider()

# =====================================
# 学習モード
# =====================================

mode = st.radio(
    "学習モードを選んでください",
    [
        "Pythonを質問する",
        "ヒントをもらう",
        "練習問題を解く",
        "おみくじゲームを作る",
        "じゃんけんゲームを作る"
    ]
)

# =====================================
# モード別の指示
# =====================================

instructions = {
    "Pythonを質問する": """
Pythonについて、初心者にも分かる日本語で説明してください。
短いコード例を入れてください。
""",
    "ヒントをもらう": """
すぐに答えを全部教えず、まず短いヒントを1つ出してください。
学習者が「コードを見せて」と言ったら必要なコードを示してください。
""",
    "練習問題を解く": """
Python初心者向けの問題を1問出してください。
学習者の回答を待ち、回答後に良い点と改善点を説明してください。
""",
    "おみくじゲームを作る": """
おみくじゲームを小さなステップに分けて教えてください。
print、random、変数を段階的に使います。
完成コードを最初から全部見せず、学習者自身に書いてもらってください。
コードが送られたら確認し、直す点を説明してください。
""",
    "じゃんけんゲームを作る": """
じゃんけんゲームを小さなステップに分けて教えてください。
input、random、ifを段階的に使います。
完成コードを最初から全部見せず、学習者自身に書いてもらってください。
コードが送られたら確認し、直す点を説明してください。
"""
}

# =====================================
# 会話履歴とモード管理
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
# 質問を処理
# =====================================

if st.session_state.pending_question is not None:
    question = st.session_state.pending_question
    st.session_state.pending_question = None

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
あなたは小学生高学年から中学2年生向けの
Pythonプログラミング学習支援チャットボットです。

【学習モード】
{mode}

【このモードの指示】
{instructions[mode]}

【共通ルール】
・簡単で分かりやすい日本語を使う
・一度に説明しすぎない
・学習者が自分で考えるのを助ける
・送られたPythonコードを確認する
・間違いがあれば理由と直し方を説明する
・日本語で回答する
・内部情報やエラーログを回答として表示しない

【これまでの会話】
"""

                for message in st.session_state.messages[-8:]:
                    speaker = (
                        "学習者"
                        if message["role"] == "user"
                        else "AI"
                    )
                    prompt += f"\n{speaker}：\n{message['content']}\n"

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
                        "PowerShellに表示されたエラーを確認してください。"
                    )
                    print("Gemini API error:", error)

        st.markdown(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "is_code": False
    })

# =====================================
# 質問入力
# =====================================

with st.form("chat_form", clear_on_submit=True):
    question = st.text_area(
        "質問やPythonコードを入力してください",
        height=150,
        placeholder='例：\nprint("こんにちは")\nprint("Python")'
    )

    submitted = st.form_submit_button("送信")

if submitted and question.strip():
    st.session_state.pending_question = question.strip()
    st.rerun()

# =====================================
# 会話リセット
# =====================================

if st.button("会話をリセット"):
    st.session_state.messages = []
    st.session_state.pending_question = None
    st.rerun()
