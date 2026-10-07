import streamlit as st
import random
import time

st.set_page_config(
    page_title="짝찾기 게임",
    page_icon="🃏",
    layout="centered"
)

# -----------------------------
# 게임 초기화
# -----------------------------
def init_game():
    emojis = ["🍎", "🍌", "🍇", "🍉", "🍓", "🍒", "🥝", "🍍"]

    cards = emojis * 2
    random.shuffle(cards)

    st.session_state.cards = cards
    st.session_state.flipped = []
    st.session_state.matched = []
    st.session_state.attempts = 0
    st.session_state.game_over = False


# 처음 실행할 때 게임 생성
if "cards" not in st.session_state:
    init_game()


# -----------------------------
# 카드 클릭
# -----------------------------
def select_card(index):
    # 이미 맞춘 카드
    if index in st.session_state.matched:
        return

    # 이미 뒤집혀 있는 카드
    if index in st.session_state.flipped:
        return

    # 두 장이 이미 선택되어 있으면 무시
    if len(st.session_state.flipped) >= 2:
        return

    st.session_state.flipped.append(index)


# -----------------------------
# 새 게임
# -----------------------------
st.title("🃏 짝찾기 게임")
st.write("같은 그림의 카드를 찾아보세요!")

if st.button("🔄 새 게임", use_container_width=True):
    init_game()
    st.rerun()


# -----------------------------
# 게임 정보
# -----------------------------
matched_count = len(st.session_state.matched) // 2
total_pairs = len(st.session_state.cards) // 2

col1, col2 = st.columns(2)

with col1:
    st.metric("🎯 맞춘 쌍", f"{matched_count} / {total_pairs}")

with col2:
    st.metric("🔢 시도 횟수", st.session_state.attempts)


# -----------------------------
# 카드 처리
# -----------------------------
if len(st.session_state.flipped) == 2:

    first, second = st.session_state.flipped

    # 같은 카드인지 확인
    if st.session_state.cards[first] == st.session_state.cards[second]:

        st.session_state.matched.extend([first, second])
        st.session_state.flipped = []

        # 모든 카드 완성
        if len(st.session_state.matched) == len(st.session_state.cards):
            st.session_state.game_over = True

    else:
        # 화면에 두 카드를 보여준 뒤 잠시 대기
        pass


# -----------------------------
# 카드 UI
# -----------------------------
st.divider()

for row in range(4):
    cols = st.columns(4)

    for col in range(4):
        index = row * 4 + col

        is_flipped = index in st.session_state.flipped
        is_matched = index in st.session_state.matched

        if is_flipped or is_matched:
            label = st.session_state.cards[index]
        else:
            label = "❓"

        with cols[col]:
            if st.button(
                label,
                key=f"card_{index}",
                use_container_width=True,
                disabled=is_matched
            ):
                select_card(index)
                st.rerun()


# -----------------------------
# 틀린 카드 처리
# -----------------------------
if len(st.session_state.flipped) == 2:

    first, second = st.session_state.flipped

    if st.session_state.cards[first] != st.session_state.cards[second]:

        st.session_state.attempts += 1

        time.sleep(0.8)

        st.session_state.flipped = []

        st.rerun()

    else:
        st.session_state.attempts += 1


# -----------------------------
# 게임 종료
# -----------------------------
if st.session_state.game_over:

    st.success(
        f"🎉 축하합니다! "
        f"{st.session_state.attempts}번 만에 모든 짝을 찾았습니다!"
    )

    if st.button("🎮 다시 플레이"):
        init_game()
        st.rerun()
