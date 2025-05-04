library(httr)
library(jsonlite)

get_identity_appeal_response <- function(text_input, api_key) {
  prompt <- paste(
    "Search for mentions containing racial or gender identity appeals.",
    "Identity appeals include:",
    "1) Highlighting positive aspects of a community’s past and present, OR",
    "2) Discussing grievances related to a community’s past or present.",
    "Examples:",
    '1) “As a proud member of the African American community, I stand before you to celebrate our rich history and achievements.”',
    '2) “Females have faced systemic discrimination for too long. I support those who have plans to address these challenges.”',
    "Coding scheme:",
    "- 1 = racial identity appeal",
    "- 2 = gender identity appeal",
    "- 0 = neither",
    'Return ONLY this format: {"explanation":"...","code":1}',
    paste0("\n\nTEXT:\n", text_input),
    sep = "\n"
  )
  
  # Call GPT API
  response <- POST(
    url = "https://api.openai.com/v1/chat/completions",
    add_headers(`Authorization` = paste("Bearer", api_key)),
    content_type_json(),
    body = list(
      model = "gpt-4-1106-preview",
      messages = list(list(role = "user", content = prompt)),
      temperature = 0
    ),
    encode = "json"
  )
  
  res_text <- content(response, as = "parsed", encoding = "UTF-8")
  
  # Return just the message content from GPT
  return(res_text$choices[[1]]$message$content)
}


api_key <-  ""  # Your OpenAI API key
text_sample <- "As a Latina woman, I’ve experienced both cultural pride and institutional barriers."

result <- get_identity_appeal_response(text_sample, api_key)
print(result)

# Load the full dataset
df <- read.csv("", stringsAsFactors = FALSE)
n_total <- nrow(df)
df$gpt_output <- NA  # initialize new column


# Batch processing setup
batch_size <- 10
save_every <- 100  # save to file every 100 rows
total_batches <- ceiling(n_total / batch_size)

# Loop over all batches
for (batch_idx in 1:total_batches) {
  cat("Processing batch", batch_idx, "of", total_batches, "...\n")
  
  # Row indices for current batch
  start_row <- ((batch_idx - 1) * batch_size) + 1
  end_row <- min(start_row + batch_size - 1, n_total)
  
  for (i in start_row:end_row) {
    if (!is.na(df$gpt_output[i])) next  # skip if already processed
    text_input <- df$reply_clean[i]
    result <- tryCatch({
      get_identity_appeal_response(text_input, api_key)
    }, error = function(e) {
      paste("ERROR:", e$message)
    })
    df$gpt_output[i] <- result
    Sys.sleep(1.2)  # adjust to avoid hitting OpenAI rate limits
  }
  
  # Save every 100 rows as a backup
  if (batch_idx %% (save_every / batch_size) == 0 || batch_idx == total_batches) {
    write.csv(df, "reply_with_gpt_output_progress.csv", row.names = FALSE)
    cat("✔️ Saved progress at batch", batch_idx, "\n")
  }
}


