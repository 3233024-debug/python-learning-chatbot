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
