# Matching Algorithm Explained

## 🎯 The Matching Formula

The Hobby Connect app uses a sophisticated weighted algorithm to calculate compatibility between users:

```
Match Score = (Hobby Score × 70%) + (Age Score × 20%) + (Category Score × 10%)
```

## 📊 What Do Match Percentages Mean?

The match percentages (like **47%** or **44%**) you see are the **overall compatibility scores** between you and other users. These percentages indicate how compatible you are based on three key factors:

1. **Shared hobbies** (most important)
2. **Age proximity** (moderately important)
3. **Common hobby categories** (bonus factor)

**Higher percentage = Better match!**

---

## 🔍 Breaking Down Each Component

### 1️⃣ Hobby Score (70% weight) - Most Important!

This is the primary factor in determining compatibility because shared hobbies are the main reason people connect on this platform.

**Formula:**
```
Hobby Score = (Number of Common Hobbies / Your Total Hobbies) × 100
```

**How it works:**
- The algorithm compares your hobby list with another user's hobby list
- It counts how many hobbies you have in common
- It divides by YOUR total number of hobbies (not the other person's)
- Multiplies by 100 to get a percentage

**Example:**
- **You have:** Gym & Weightlifting, Drawing, Cooking (3 hobbies)
- **Other user has:** Gym & Weightlifting, Drawing, Cooking, Gaming (4 hobbies)
- **Common hobbies:** 3 match
- **Calculation:** (3 / 3) × 100 = **100%**
- **Weighted contribution:** 100 × 0.70 = **70 points**

**Another example:**
- **You have:** Photography, Hiking, Cooking, Gaming (4 hobbies)
- **Other user has:** Photography, Reading (2 hobbies)
- **Common hobbies:** 1 match (Photography)
- **Calculation:** (1 / 4) × 100 = **25%**
- **Weighted contribution:** 25 × 0.70 = **17.5 points**

**Key insight:** The more of YOUR hobbies that match with someone else's, the higher the score. This is calculated from your perspective.

---

### 2️⃣ Age Proximity Score (20% weight)

People tend to connect better with others in a similar age range. This component rewards closer ages.

**Formula:**
```
Age Score = ((Max Difference - Actual Difference) / Max Difference) × 100
```
Where **Max Difference = 30 years**

**How it works:**
- Calculates the absolute age difference between you and another user
- The smaller the difference, the higher the score
- If age difference is ≥30 years, the score is 0%
- Otherwise, it scales from 0% to 100% based on proximity

**Example 1:**
- **Your age:** 24 years old
- **Other user's age:** 22 years old
- **Age difference:** |24 - 22| = 2 years
- **Calculation:** ((30 - 2) / 30) × 100 = **93.3%**
- **Weighted contribution:** 93.3 × 0.20 = **18.7 points**

**Example 2:**
- **Your age:** 25 years old
- **Other user's age:** 40 years old
- **Age difference:** |25 - 40| = 15 years
- **Calculation:** ((30 - 15) / 30) × 100 = **50%**
- **Weighted contribution:** 50 × 0.20 = **10 points**

**Example 3:**
- **Your age:** 22 years old
- **Other user's age:** 22 years old (same age!)
- **Age difference:** 0 years
- **Calculation:** ((30 - 0) / 30) × 100 = **100%**
- **Weighted contribution:** 100 × 0.20 = **20 points**

**Key insight:** Same age gets maximum points (20). As the age gap increases, points decrease gradually until 30+ years gets 0 points.

---

### 3️⃣ Category Score (10% weight)

This is a bonus component that rewards users who share similar types of hobbies, even if the specific hobbies differ.

**Formula:**
```
Category Score = (Common Categories / Your Total Categories) × 100
```

**Hobby Categories:**
- Sports & Fitness
- Creative Arts
- Music
- Technology
- Outdoor
- Social
- Intellectual

**How it works:**
- Groups your hobbies into categories
- Compares which categories you share with another user
- Similar to hobby scoring, but at the category level

**Example:**
- **Your hobbies:**
  - Gym & Weightlifting (Sports & Fitness)
  - Drawing (Creative Arts)
  - Cooking (Social)
  - **Your categories:** Sports & Fitness, Creative Arts, Social (3 categories)
  
- **Other user's hobbies:**
  - Running (Sports & Fitness)
  - Painting (Creative Arts)
  - Gaming (Technology)
  - **Their categories:** Sports & Fitness, Creative Arts, Technology (3 categories)

- **Common categories:** Sports & Fitness, Creative Arts (2 match)
- **Calculation:** (2 / 3) × 100 = **66.7%**
- **Weighted contribution:** 66.7 × 0.10 = **6.7 points**

**Key insight:** This ensures that even if you don't share exact hobbies, having similar types of interests provides a small bonus.

---

## 💡 Complete Example: Understanding a 47% Match

Let's calculate exactly how a **47% match** could be achieved:

### Scenario:
- **Your profile:**
  - Age: 24
  - Hobbies: Gym & Weightlifting, Drawing, Cooking, Reading, Photography (5 hobbies)
  - Categories: Sports & Fitness, Creative Arts, Social, Intellectual (4 categories)

- **Other user's profile:**
  - Age: 22
  - Hobbies: Gym & Weightlifting, Drawing, Cooking (3 hobbies)
  - Categories: Sports & Fitness, Creative Arts, Social (3 categories)

### Calculations:

**1. Hobby Score:**
- Common hobbies: 3 (Gym, Drawing, Cooking)
- Your total hobbies: 5
- Score: (3 / 5) × 100 = **60%**
- Weighted: 60 × 0.70 = **42 points**

**2. Age Proximity Score:**
- Age difference: |24 - 22| = 2 years
- Score: ((30 - 2) / 30) × 100 = **93.3%**
- Weighted: 93.3 × 0.20 = **18.7 points**

**3. Category Score:**
- Common categories: 3 (Sports, Creative, Social)
- Your total categories: 4
- Score: (3 / 4) × 100 = **75%**
- Weighted: 75 × 0.10 = **7.5 points**

### Total Match Score:
```
42 + 18.7 + 7.5 = 68.2%
```

*Note: Actual match percentages in your app depend on the specific hobbies and ages of the logged-in user.*

---

## 📈 Score Interpretation Guide

Understanding what different match percentages mean:

| Match % | Rating | Meaning | Recommendation |
|---------|--------|---------|----------------|
| **90-100%** | 🔥🔥🔥 Exceptional | Nearly identical interests and age | Highly recommended - reach out! |
| **80-89%** | 🔥🔥 Excellent | Very similar interests, close age | Great potential for connection |
| **70-79%** | 🔥 Very Good | Many shared hobbies | Good match - worth exploring |
| **60-69%** | ✅ Good | Several common interests | Solid match with good potential |
| **50-59%** | 👍 Moderate | Some shared hobbies | Decent compatibility |
| **40-49%** | 🤔 Fair | A few common interests | Some common ground exists |
| **30-39%** | 😐 Low | Minimal shared hobbies | Limited compatibility |
| **20-29%** | 👎 Very Low | Very few similarities | Unlikely to connect |
| **0-19%** | ❌ Minimal | Almost no shared interests | Poor match |

### Your Matches:
- **Shray: 47%** = Fair match - You have some common hobbies
- **Premanshu: 44%** = Fair match - Similar to Shray, decent overlap

Both showing 3 common hobbies: Gym & Weightlifting, Drawing, Cooking

---

## 🎲 Why This Formula Works

### Weight Distribution Rationale:

**70% for Hobbies:**
- Primary reason people use this app
- Direct indicator of shared interests
- Most important for starting conversations

**20% for Age:**
- Helps find people in similar life stages
- Important for compatibility
- Not the main factor, but significant

**10% for Categories:**
- Bonus for similar interest types
- Helps when exact hobbies don't match
- Encourages exploration of new hobbies

### Algorithm Benefits:

1. **User-Centric:** Calculated from YOUR perspective (your hobby count in denominator)
2. **Balanced:** Weighs multiple factors, not just one criterion
3. **Fair:** Everyone can get matches regardless of age or hobby count
4. **Intuitive:** Higher numbers = better matches
5. **Inclusive:** Only shows matches with at least 1 common hobby

---

## 🔧 Technical Implementation

The matching algorithm is implemented in:
- **Backend:** `backend/app/services/matching_service.py`
- **Class:** `MatchingService`
- **Main Method:** `calculate_match_percentage(user, other_user)`

### Key Features:
- Filters out users with zero common hobbies
- Applies age range filters if specified
- Applies minimum match percentage filter
- Sorts results by match percentage (descending)
- Supports pagination for large result sets

---

## 🚀 Using the Match Filters

On the Find Matches page, you can refine your results:

### 1. Age Range Filter
- Set minimum and maximum age
- Example: 18-30 to find matches in your age group

### 2. Minimum Match % Filter
- Set a threshold (0-100%)
- Example: Set to 50% to only see moderate or better matches

### 3. Sort Options
- **Match %** (default): Shows best matches first
- **Age**: Sorts by age
- **Name**: Alphabetical sorting

---

## 📝 Tips for Better Matches

1. **Add more hobbies:** More hobbies = more potential matches
2. **Be specific:** Select your actual interests, not what you think others want
3. **Try categories:** Explore hobbies in categories you enjoy
4. **Update regularly:** Keep your hobby list current
5. **Lower filters:** If you're not seeing matches, reduce the minimum match percentage
6. **Expand age range:** A wider age range increases potential matches

---

## ❓ FAQ

**Q: Why is someone with more common hobbies showing a lower percentage than someone with fewer?**
A: The algorithm considers all three factors (hobbies, age, categories). Age proximity and category matches can boost scores even with fewer common hobbies.

**Q: Can I get a 100% match?**
A: Yes! You'd need 100% hobby overlap, same age, and 100% category overlap.

**Q: What's a "good enough" match to connect with someone?**
A: Anything above 40% indicates some shared interests. Don't be afraid to reach out even with moderate matches!

**Q: Why don't I see everyone in the database?**
A: The algorithm only shows users with at least 1 common hobby. Users with zero shared hobbies are filtered out.

**Q: Does the other person see the same match percentage with me?**
A: Not necessarily! Since the hobby score uses YOUR hobby count, if you have different numbers of hobbies, the percentages will differ.

---

## 📚 References

For more technical details, see:
- [README.md](README.md) - Overview of the entire application
- [PROJECT_ARCHITECTURE.md](PROJECT_ARCHITECTURE.md) - Detailed architecture documentation
- [backend/app/services/matching_service.py](backend/app/services/matching_service.py) - Source code

---

*Last updated: March 6, 2026*
