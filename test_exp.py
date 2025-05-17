from experience_extractor import extract_experience

experience = extract_experience("kunalResume.pdf")
print("🎯 Experience Section Found:")
print(experience["raw_text"])
print("\n🔹 Highlights:")
for h in experience["highlights"]:
    print("-", h)
