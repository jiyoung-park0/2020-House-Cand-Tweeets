#pip install --upgrade openai
import os
import re
import pandas as pd
from sklearn.model_selection import train_test_split
from openai import OpenAI

# Set up OpenAI API key
os.environ["OPENAI_API_KEY"] = "[Your OpenAI API key]"
client = OpenAI()

# Load data
#data = pd.read_csv('Tweets_candidate_info.csv')

data = pd.read_csv('New_Tweets_candidate_info.csv')       # Resume from where it stopped

original_tweet_data = data['original_tweet']

# Define function to remove numbers, links, %, @ from text
def clean_text(text):
    # Remove links
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    # Remove emails
    text = re.sub(r'\S+@\S+', '', text)
    # Remove % symbol
    text = re.sub(r'%', '', text)
    # Remove @ symbol and usernames
    text = re.sub(r'@\w+', '', text)
    # Remove numbers
    text = re.sub(r'\d+', '', text)

    # Added on 08-09

    # Remove dollar sign
    text = re.sub(r'\$', '', text)
    
    # Remove & symbol
    text = re.sub(r'&', '', text)

    return text

# Remove numbers, links, %, @ from original_tweet
cleaned_tweet_data = original_tweet_data.apply(clean_text)

# Check if numbers remain in the cleaned data
remaining_numbers = cleaned_tweet_data[cleaned_tweet_data.str.contains(r'\d', na=False)]
print("Number of tweets with remaining numbers after cleaning:", len(remaining_numbers))

# Check if % symbols remain in the cleaned data
remaining_percent = cleaned_tweet_data[cleaned_tweet_data.str.contains(r'%', na=False)]
print("Number of tweets with remaining % symbols after cleaning:", len(remaining_percent))

# Check if @ symbols remain in the cleaned data
remaining_at = cleaned_tweet_data[cleaned_tweet_data.str.contains(r'@', na=False)]
print("Number of tweets with remaining @ symbols after cleaning:", len(remaining_at))

# Print examples of tweets with remaining numbers, %, @ symbols
print("\nExamples of tweets with remaining numbers:")
print(remaining_numbers.head())

print("\nExamples of tweets with remaining % symbols:")
print(remaining_percent.head())

print("\nExamples of tweets with remaining @ symbols:")
print(remaining_at.head())

# Convert the entire data to a dataframe (skip data splitting and use the entire dataset)
train_data = cleaned_tweet_data.to_frame(name='original_tweet')

# Check for NaN values
nan_count = train_data.isnull().sum().sum()
print("Number of NaN values:", nan_count)

# Print rows with NaN values
nan_rows = train_data[train_data.isnull().any(axis=1)]
print("Rows with NaN values:")
print(nan_rows)

# Train text classification model using OpenAI
def classify_identity(text):
    content = "Search for mentions containing racial or gender identity appeals. Identity appeals include 1) highlighting positive aspects of a community's past and present or 2) discussing grievances related to a community's past or present. Code mentions as follows: 1 for racial identity appeal, 2 for gender identity appeal, and 0 for neither case.\n\nText: {0}\n\n".format(text)
    
    # Get API response
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[                                                                                                                                                                                                                                                              
            {"role": "system", "content": "You are a specialist in identity recognition and text classification."},   # Assign persona
            {"role": "user", "content": content}
        ]
    )
    
    # Extract content from response
    message = response.choices[0].message.content
    
    # Extract numbers from content string
    category = re.sub(r'[^0-3]', '', message)
    return category  # Return result

# List to store classification results
classified_results = []

# Perform classification for each text
save_interval = 100  # Set how often to save
for idx, reply in enumerate(train_data['original_tweet']):
    try:
        category = classify_identity(reply)
        classified_results.append(category)
        
        # Save progress at specified intervals
        if (idx + 1) % save_interval == 0:
            temp_train_data = train_data.iloc[:len(classified_results)].copy()
            temp_train_data['category'] = classified_results
            temp_train_data.to_csv('results_partial_temp_0810.csv', index=False)
            print(f"Progress saved at {idx + 1} entries.")
        
    except Exception as e:
        print(f"Error processing origin: {reply}\n{e}")
        break  # Exit loop if interrupted

# Add classification results to training data
train_data = train_data.iloc[:len(classified_results)]  # Use only the results obtained so far
train_data['category'] = classified_results

# Save final results to CSV file
train_data.to_csv('GPT_TextClassification_origin_3.csv', index=False)