# -*- coding: utf-8 -*-
"""
Created on Sat Jan 31 11:16:53 2026

@author: mbuya
"""

def calculate_balance_score(study, sleep, social, screen, stress):
    score = 0

    # Study
    if 2 <= study <= 6:
        score += 20
    elif study > 6:
        score += 15
    else:
        score += 10

    # Sleep
    if 7 <= sleep <= 9:
        score += 25
    elif 5 <= sleep < 7:
        score += 15
    else:
        score += 5

    # Social
    if 1 <= social <= 3:
        score += 15
    else:
        score += 8

    # Screen
    if screen <= 4:
        score += 15
    elif screen <= 8:
        score += 10
    else:
        score += 5

    # Stress
    if stress <= 3:
        score += 15
    elif stress <= 6:
        score += 10
    else:
        score += 5

    return score


def mental_state(score):
    if score >= 80:
        return "🟢 Excellent Balance"
    elif score >= 60:
        return "🟡 Moderate Balance"
    elif score >= 40:
        return "🟠 Unstable Balance"
    else:
        return "🔴 Critical State"


def advice_generator(study, sleep, social, screen, stress):
    tips = []

    if sleep < 7:
        tips.append("😴 Try to get more sleep for better mental health.")
    if study < 2:
        tips.append("📚 Increase study consistency.")
    if screen > 6:
        tips.append("📵 Reduce screen time.")
    if stress > 6:
        tips.append("🧘 Manage stress with rest and exercise.")
    if social < 1:
        tips.append("🧑‍🤝‍🧑 Increase social interaction.")

    if not tips:
        tips.append("✅ You are maintaining a healthy balance.")

    return tips
