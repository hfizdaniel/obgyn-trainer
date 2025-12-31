"""
OB/GYN Trainer
Copyright (c) 2025 Hafiz Daniel

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""




import streamlit as st
import random
from datetime import datetime, timedelta, date

# --- 1. Page Config ---
st.set_page_config(page_title="OB/GYN Calculation Trainer", page_icon="🩺", layout="centered")

# --- 2. MODERN UI & CSS ---
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background-color: #0E1117;
        background-image: linear-gradient(to bottom, #0E1117, #161b22);
        color: #FAFAFA;
    }
    
    /* Card Container */
    .css-card {
        background-color: #1F2937;
        padding: 2rem;
        border-radius: 15px;
        border: 1px solid #374151;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
        text-align: center;
    }
    
    /* Logic Step Styling */
    .logic-step {
        background-color: #262730;
        border-left: 4px solid #60A5FA; 
        padding: 12px 18px;
        margin-bottom: 12px;
        border-radius: 0 8px 8px 0;
        line-height: 1.6;
    }
    .logic-hint {
        background-color: #422006; 
        border-left: 4px solid #F59E0B; 
        padding: 12px 18px;
        margin-bottom: 12px;
        border-radius: 0 8px 8px 0;
        color: #FCD34D; 
        font-size: 0.95em;
    }
    .logic-final {
        background-color: #064E3B; 
        border-left: 4px solid #34D399; 
        padding: 15px;
        border-radius: 0 8px 8px 0;
        font-weight: bold;
        font-size: 1.1em;
        margin-top: 10px;
    }

    /* Input Fields */
    div[data-baseweb="select"] > div {
        background-color: #374151;
        color: white;
        border-color: #4B5563;
        border-radius: 8px;
    }
    .stTextInput > div > div > input {
        background-color: #374151;
        color: white;
        border-radius: 8px;
        border: 1px solid #4B5563;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 28px !important;
        font-weight: 700;
        color: #60A5FA;
    }
    
    /* Buttons */
    div.stButton > button {
        width: 100%;
        border-radius: 10px;
        background-color: #2563EB;
        color: white;
        font-weight: 600;
        border: none;
        padding: 12px 20px;
    }
    div.stButton > button:hover {
        background-color: #1D4ED8;
    }
            
    /* --- NEW: BIGGER RADIO BUTTONS (FIXED) --- */
    
    /* 1. The Question Label */
    div[data-testid="stRadio"] > label {
        font-size: 24px !important;
        font-weight: 800 !important;
        color: #60A5FA !important;
        margin-bottom: 15px !important;
    }
    
    /* 2. The Options Text (Targeting the <p> tag inside is key) */
    div[data-testid="stRadio"] div[role="radiogroup"] p {
        font-size: 20px !important;
        font-weight: 500 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. Helper Functions ---
def generate_random_date(start_year, end_year):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    delta = end - start
    random_days = random.randrange(delta.days)
    return (start + timedelta(days=random_days)).date()

def format_date(d):
    return d.strftime("%d/%m/%Y")

def subtract_months(dt, months):
    month = dt.month - 1 - months
    year = dt.year + month // 12
    month = month % 12 + 1
    day = min(dt.day, [31,
        29 if year % 4 == 0 and not year % 100 == 0 or year % 400 == 0 else 28,
        31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1])
    return dt.replace(year=year, month=month, day=day)

def get_month_days(year, month):
    if month == 2:
        if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0): return 29
        return 28
    elif month in [1, 3, 5, 7, 8, 10, 12]: return 31
    else: return 30

# --- NEW: Dropdown Input Function ---
def dropdown_date_input(label_key, default_date=None):
    if default_date is None:
        default_date = date.today()

    # Layout: Day | Month | Year
    c1, c2, c3 = st.columns([1, 1.3, 1.1])
    
    with c3:
        # Year (Current year -1 to +2)
        years = list(range(2024, 2031))
        # Ensure default year is in range
        start_y_index = 0
        if default_date.year in years:
            start_y_index = years.index(default_date.year)
        
        sel_y = st.selectbox("Year", years, index=start_y_index, key=f"{label_key}_y", label_visibility="collapsed")
    
    with c2:
        # Month
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        sel_m_str = st.selectbox("Month", months, index=default_date.month-1, key=f"{label_key}_m", label_visibility="collapsed")
        sel_m = months.index(sel_m_str) + 1
    
    with c1:
        # Day (Dynamic based on Month/Year)
        max_days = get_month_days(sel_y, sel_m)
        days = list(range(1, max_days + 1))
        
        # Try to keep the previous day selection if possible
        default_d_index = default_date.day - 1
        if default_d_index >= len(days):
            default_d_index = len(days) - 1
            
        sel_d = st.selectbox("Day", days, index=default_d_index, key=f"{label_key}_d", label_visibility="collapsed")
        
    return date(sel_y, sel_m, sel_d)


def generate_human_logic_html(start_date, end_date):
    """
    Simulates a 'Start Fragment -> Middle Blocks -> End Fragment' walkthrough.
    Fixed to ensure days sum up exactly to (end - start).days
    """
    total_days = (end_date - start_date).days
    
    # 1. Short Gap Strategy (< 28 days)
    if total_days < 28:
         weeks = total_days // 7
         days = total_days % 7
         
         countdown_w = 40 - weeks
         if days > 0:
             countdown_w -= 1
             countdown_d = 7 - days
         else:
             countdown_d = 0
             
         return f"""
         <div class="logic-hint"><strong>⚡ Short Gap Strategy</strong><br>Less than a month. Just count weeks directly.</div>
         <div class="logic-step"><strong>1. The Gap</strong><br>{total_days} days.</div>
         <div class="logic-step"><strong>2. Weeks</strong><br>{total_days} ÷ 7 = <strong>{weeks}w {days}d</strong>.</div>
         <div class="logic-final">Countdown: 40w 0d - {weeks}w {days}d = <strong>{countdown_w}w {countdown_d}d</strong></div>
         """

    # 2. Long Gap Strategy (The Month Walk)
    html_output = """<div class="logic-hint">
        <strong>⚡ Strategy: The "Month Walk"</strong><br>
        1. Rest of current month.<br>2. Full middle months.<br>3. Days in final month.
    </div>
    <div class="logic-step"><strong>1. Walk through the calendar</strong><br>"""
    
    # --- Logic Calculation ---
    accum_surplus_days = 0
    accum_weeks_from_months = 0
    
    # A. Start Fragment (Rest of the starting month)
    days_in_start = get_month_days(start_date.year, start_date.month)
    start_frag = days_in_start - start_date.day
    
    # Check if we are strictly within one month
    if start_date.year == end_date.year and start_date.month == end_date.month:
        start_frag = end_date.day - start_date.day
    
    if start_frag > 0:
        html_output += f"• Rest of {start_date.strftime('%B')}: <strong>{start_frag}d</strong><br>"
        accum_surplus_days += start_frag
    elif start_frag == 0:
        html_output += f"• Rest of {start_date.strftime('%B')}: <strong>0d</strong> (End of month)<br>"

    # B. Middle Blocks
    cursor = (start_date.replace(day=1) + timedelta(days=32)).replace(day=1)
    
    while (cursor.year < end_date.year) or (cursor.year == end_date.year and cursor.month < end_date.month):
        days_in_curr = get_month_days(cursor.year, cursor.month)
        surplus = days_in_curr - 28
        month_name = cursor.strftime("%B")
        
        if surplus == 3: html_output += f"• <strong>{month_name}</strong> (Big) = 4w + <strong>3d</strong><br>"
        elif surplus == 2: html_output += f"• <strong>{month_name}</strong> (Small) = 4w + <strong>2d</strong><br>"
        elif surplus == 1: html_output += f"• <strong>{month_name}</strong> (Leap) = 4w + <strong>1d</strong><br>"
        else: html_output += f"• <strong>{month_name}</strong> (Feb) = 4w + <strong>0d</strong><br>"
        
        accum_weeks_from_months += 4
        accum_surplus_days += surplus
        
        cursor = (cursor.replace(day=1) + timedelta(days=32)).replace(day=1)

    # C. End Fragment
    if cursor.year == end_date.year and cursor.month == end_date.month:
        end_frag = end_date.day
        html_output += f"• Days in {end_date.strftime('%B')}: <strong>{end_frag}d</strong><br>"
        accum_surplus_days += end_frag

    html_output += "</div>"
    
    # --- Tally ---
    surplus_weeks = accum_surplus_days // 7
    surplus_remainder = accum_surplus_days % 7
    
    total_gap_weeks = accum_weeks_from_months + surplus_weeks
    total_gap_days = surplus_remainder
    
    html_output += f"""<div class="logic-step"><strong>2. Tally Up</strong><br>
    • Weeks from Months: <strong>{accum_weeks_from_months}w</strong><br>
    • Loose Days Sum: <strong>{accum_surplus_days}d</strong><br>
    • Simplify: {accum_weeks_from_months}w + {surplus_weeks}w {surplus_remainder}d = <strong>{total_gap_weeks}w {total_gap_days}d</strong> gap.
    </div>"""
    
    # --- Countdown ---
    final_poa_w = 40 - total_gap_weeks
    if total_gap_days > 0:
        final_poa_w -= 1
        final_poa_d = 7 - total_gap_days
    else:
        final_poa_d = 0
        
    html_output += f"""<div class="logic-final"><strong>3. The Countdown (40w - Gap)</strong><br>
    40w 0d − {total_gap_weeks}w {total_gap_days}d = <strong>{final_poa_w}w {final_poa_d}d</strong>
    </div>"""
    
    return html_output

# --- 4. Session State ---
if 'lmp' not in st.session_state:
    st.session_state['lmp'] = None
if 'redd_start' not in st.session_state:
    st.session_state['redd_start'] = None
if 'redd_target' not in st.session_state:
    st.session_state['redd_target'] = None

# --- 5. Main App Layout ---
col1, col2 = st.columns([1, 2]) 
with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/14373/14373989.png", width=200)

with col2:
    st.title("OB/GYN Gestational Age and EDD Trainer")
    st.caption("Created by Hafiz Daniel | 5th Year Med Student")
    st.markdown("""
    <div style="font-style: italic; color: #9CA3AF; font-size: 0.85em; margin-top: 5px;">
        “Wherever the art of Medicine is loved, there is also a love of humanity.”<br>
        ― Hippocrates
    </div>
    """, unsafe_allow_html=True)

st.write("") 

mode = st.radio("Select Training Mode:", 
                ["🤰 EDD (Naegele's Rule)", "👶 Gestational Age (from REDD)"],
                horizontal=True)
st.markdown("---")

# ===========================
# MODE 1: EDD CALCULATOR
# ===========================
if mode == "🤰 EDD (Naegele's Rule)":
    
    st.markdown("##### 1️⃣ Select LMP Source")
    case_type = st.radio("Case Source:", ["🎲 Randomize", "✏️ Custom"], horizontal=True, label_visibility="collapsed", key="edd_source")
    
    if case_type == "🎲 Randomize":
        if st.button("🔄 Generate New Date"):
            st.session_state['lmp'] = generate_random_date(2025, 2027)
    else:
        # --- MODIFICATION: Using new dropdown input ---
        st.write("Select Date:")
        # We pass date.today() as default
        custom_lmp = dropdown_date_input("lmp_input", default_date=date.today())
        
        # In this simple version, we just assign it. 
        # Streamlit re-runs on every select change, so this works naturally.
        st.session_state['lmp'] = custom_lmp

    st.write("")
    st.write("")

    if st.session_state['lmp']:
        lmp = st.session_state['lmp']
        
        st.markdown(f"""
        <div class="css-card">
            <h4 style="margin:0; color:#9CA3AF; font-size:14px;">PATIENT LMP</h4>
            <h1 style="margin:10px 0 0 0; color:#FAFAFA; font-size: 3rem;">{format_date(lmp)}</h1>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("##### 2️⃣ What is the EDD?")
        input_type = st.radio("Input Method:", ["📅 Calendar", "⌨️ Manual Typing"], horizontal=True, label_visibility="collapsed")
        
        user_date = None
        if input_type == "📅 Calendar":
            # --- MODIFICATION: Using new dropdown input ---
            # Default to LMP + 9 months to be helpful
            approx_edd = lmp + timedelta(days=280)
            user_date = dropdown_date_input("edd_input", default_date=approx_edd)
        else:
            date_str = st.text_input("Type EDD", placeholder="DD/MM/YYYY", key="edd_input_text")
            if date_str:
                try:
                    user_date = datetime.strptime(date_str, "%d/%m/%Y").date()
                except ValueError:
                    st.warning("⚠️ Invalid format. Please use DD/MM/YYYY")

        st.write("") 
        
        if st.button("✅ Submit", key="submit_edd"):
            if user_date:
                correct_edd = lmp + timedelta(days=280)
                diff = abs((user_date - correct_edd).days)
                
                step1_year = lmp.replace(year=lmp.year + 1)
                step2_months = subtract_months(step1_year, 3)
                
                if diff <= 3:
                    st.success(f"**Correct!** (Within {diff} days)")
                    st.balloons()
                else:
                    st.error(f"**Incorrect.** You were off by {diff} days.")
                
                c1, c2 = st.columns(2)
                c1.metric("Your Answer", format_date(user_date))
                c2.metric("Exact 280 Days", format_date(correct_edd))
                
                with st.expander("📝 View Step-by-Step Logic", expanded=True):
                    st.markdown(f"""
                    <div class="logic-step">
                        <strong>Step 1: LMP</strong><br>
                        {format_date(lmp)}
                    </div>
                    <div class="logic-step">
                        <strong>Step 2: Add 1 Year</strong><br>
                        {format_date(step1_year)}
                    </div>
                    <div class="logic-step">
                        <strong>Step 3: Subtract 3 Months</strong><br>
                        {format_date(step2_months)}
                    </div>
                    <div class="logic-step">
                        <strong>Step 4: Add 7 Days</strong><br>
                        {format_date(step2_months + timedelta(days=7))}
                    </div>
                    <div class="logic-final">
                        <strong>Computer Exact (280 Days):</strong><br>
                        {format_date(correct_edd)}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    is_leap = False
                    curr = lmp
                    while curr <= correct_edd:
                        if curr.month == 2 and curr.day == 29:
                            is_leap = True
                            break
                        curr += timedelta(days=1)
                    
                    if is_leap:
                         st.markdown("""
                         <div class="leap-warning">
                             ⚠️ <strong>LEAP YEAR DETECTED (FEB 29)</strong><br>
                             This calculation crossed a leap day!
                         </div>
                         """, unsafe_allow_html=True)

            else:
                st.warning("Please enter a date first.")

# ===========================
# MODE 2: GESTATIONAL AGE
# ===========================
else:
    st.markdown("##### 1️⃣ Select Case Source")
    case_type_ga = st.radio("Case Source:", ["🎲 Randomize", "✏️ Custom"], horizontal=True, label_visibility="collapsed", key="ga_source")
    

    if case_type_ga == "🎲 Randomize":
        # New filter option
        near_term = st.checkbox("🎯 Focus on Near Term (>30 Weeks)")
        
        if st.button("🔄 Generate REDD Case"):
            st.session_state['redd_start'] = generate_random_date(2025, 2027)
            
            if near_term:
                # Less than 70 days remaining = More than 30 weeks gestation
                days_to_due = random.randint(1, 70)
            else:
                # Standard range (roughly 4 weeks to 40 weeks)
                days_to_due = random.randint(7, 250)
                
            st.session_state['redd_target'] = st.session_state['redd_start'] + timedelta(days=days_to_due)
    else:
        # --- MODIFICATION: Dropdowns for GA Mode ---
        st.write("Current Date:")
        custom_current = dropdown_date_input("ga_current_input", default_date=date.today())
        
        st.write("REDD (Due Date):")
        custom_redd = dropdown_date_input("ga_redd_input", default_date=date.today() + timedelta(days=280))
        
        st.session_state['redd_start'] = custom_current
        st.session_state['redd_target'] = custom_redd

    st.write("")
    
    if st.session_state['redd_start'] and st.session_state['redd_target']:
        current = st.session_state['redd_start']
        redd = st.session_state['redd_target']
        
        c1, c2 = st.columns(2)
        with c1:
             st.markdown(f"""
            <div class="css-card" style="padding: 1.5rem;">
                <h4 style="margin:0; color:#9CA3AF; font-size:12px;">CURRENT DATE</h4>
                <h2 style="margin:5px 0 0 0; color:#FAFAFA;">{format_date(current)}</h2>
            </div>
            """, unsafe_allow_html=True)
        with c2:
             st.markdown(f"""
            <div class="css-card" style="padding: 1.5rem; border-color: #60A5FA;">
                <h4 style="margin:0; color:#60A5FA; font-size:12px;">REDD (DUE DATE)</h4>
                <h2 style="margin:5px 0 0 0; color:#FAFAFA;">{format_date(redd)}</h2>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("### 📝 Calculate POA")
        
        ic1, ic2 = st.columns(2)
        with ic1:
            u_weeks = st.number_input("Weeks", 0, 42, step=1)
        with ic2:
            u_days = st.number_input("Days", 0, 6, step=1)
            
        if st.button("✅ Submit", key="submit_ga"):
            days_remaining = (redd - current).days
            days_elapsed = 280 - days_remaining
            correct_w = days_elapsed // 7
            correct_d = days_elapsed % 7
            
            # 1. CHECK: Negative Age (Time Traveler)
            if correct_w < 0:
                st.write("")
                st.error("🛑 **Hold on, Time Traveller!** 🏎️💨")
                st.write("")
                st.markdown(f"""
                <div style="text-align: center; padding: 40px; border: 2px dashed #ff4b4b; border-radius: 15px; margin-bottom: 30px;">
                    <h1 style="font-size: 60px; margin: 0;">👶🚫</h1>
                    <h2 style="color: #ff4b4b; font-size: 35px; margin-top: 10px;">Babies can't have negative age!</h2>
                    <p style="font-size: 22px; margin-top: 20px; line-height: 1.5;">
                        You are calculating for a date <strong>before the baby was even conceived.</strong><br>
                        Unless this is a sci-fi movie, check your years!
                    </p>
                </div>
                """, unsafe_allow_html=True)

            # 2. CHECK: Super Post-Term (Elephant)
            elif correct_w > 50:
                st.write("")
                st.error("🛑 **Whoa, that's a long time!** 🐘")
                st.write("")
                st.markdown(f"""
                <div style="text-align: center; padding: 40px; border: 2px dashed #ff4b4b; border-radius: 15px; margin-bottom: 30px;">
                    <h1 style="font-size: 60px; margin: 0;">🎒📅</h1>
                    <h2 style="color: #ff4b4b; font-size: 35px; margin-top: 10px;">Is this baby going to school?</h2>
                    <p style="font-size: 22px; margin-top: 20px; line-height: 1.5;">
                        You calculated <strong>{correct_w} weeks!</strong><br>
                        Unless your patient is an Elephant (22 months gestation),<br>
                        please check your dates!
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            # 3. CHECK: Correct Answer
            elif u_weeks == correct_w and u_days == correct_d:
                st.success("**Correct!** Spot on.")
                st.balloons()

            # 4. CHECK: Incorrect Answer
            else:
                st.error("**Incorrect.**")
                st.metric("Correct POA", f"{correct_w}w + {correct_d}d")
            
            # --- MENTAL MATH STRATEGY (Only show if date is valid) ---
            if 0 <= correct_w <= 50:
                with st.expander("🧠 Mental Math Strategy (How to think)", expanded=True):
                    if days_remaining < 105:
                         st.markdown(generate_human_logic_html(current, redd), unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="logic-hint">
                            <strong>Strategy: "The Count Up"</strong><br>
                            Since it's early, counting forward is safer than subtracting backwards.
                        </div>
                        <div class="logic-step">
                            <strong>1. Total Days Passed</strong><br>
                            280 (Full Term) − {days_remaining} (Remaining) = <strong>{days_elapsed} days</strong>.
                        </div>
                        <div class="logic-step">
                            <strong>2. Convert to Weeks</strong><br>
                            {days_elapsed} ÷ 7 = <strong>{correct_w} weeks</strong>.
                        </div>
                         <div class="logic-step">
                            <strong>3. Remainder</strong><br>
                            Leftover days = <strong>{correct_d} days</strong>.
                        </div>
                         <div class="logic-final">
                            Result: {correct_w}w + {correct_d}d
                        </div>
                        """, unsafe_allow_html=True)
# --- 6. FOOTER & REFERENCE AREA ---
st.write("")
st.write("")
st.markdown("---") 

st.markdown("<h3 style='text-align: center;'>📚 Cheat Sheet</h3>", unsafe_allow_html=True)

# Define the HTML as a single string first to avoid indentation errors
cheat_sheet_html = """
<div style="background-color: rgba(255, 75, 75, 0.15); border: 1px solid #ff4b4b; padding: 20px; border-radius: 10px; margin-bottom: 25px;">
    <div style="text-align: center; margin-bottom: 15px;">
        <strong style="color: #ff4b4b; font-size: 18px;">🛑 Prerequisites for Naegele's Rule</strong>
    </div>
    <ul style="margin: 0; padding-left: 20px; color: #ffdede;">
        <li><strong>Sure of Date:</strong> Patient remembers LMP clearly.</li>
        <li><strong>Regular Cycles:</strong> 28 days (+/- few days).</li>
        <li><strong>No Hormonal Contraception:</strong> Stopped >3 months ago.</li>
        <li><strong>No Breastfeeding:</strong> No lactational amenorrhea (within 6 months postpartum)</li>
    </ul>
    <hr style="border-color: rgba(255,75,75,0.3); margin: 15px 0;">
    <div style="text-align: center;">
        <strong style="color: #60A5FA;">🧮 The Formula</strong><br>
        <span style="font-size: 18px; font-family: monospace;">EDD = LMP + 7 days − 3 months ± 1 year</span>
    </div>
</div>
"""

st.markdown(cheat_sheet_html, unsafe_allow_html=True)

ref1, ref2, ref3 = st.columns(3)

with ref1:
    st.info("**📅 Mental Math Tricks**")
    st.markdown("""
    * **Big Month:** 4w + 3d
    * **Small Month:** 4w + 2d
    * **Feb:** 4w exactly
    """)

with ref2:
    st.warning("**⚠️ Preterm Definitions**")
    st.markdown("""
    * **Viability:** ~24 weeks
    * **Extreme:** < 28w
    * **Very:** 28w - 32w
    * **Late:** 32w - 37w
    """)

with ref3:
    st.success("**✅ Term Classifications**")
    st.markdown("""
    * **Early Term:** 37w - 38w+6
    * **Full Term:** 39w - 40w+6
    * **Late Term:** 41w - 41w+6
    * **Post Term:** ≥ 42w
    """)

st.markdown("""
<div style="text-align: center; margin-top: 50px; color: #6B7280; font-size: 12px;">
    FOR EDUCATIONAL PURPOSES ONLY. NOT FOR CLINICAL DIAGNOSIS.<br>
    © 2025 OB/GYN Trainer v1.3
</div>
""", unsafe_allow_html=True)