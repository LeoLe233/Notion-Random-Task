# Notion Random Task Generator

A Python tool that automatically generates daily tasks in Notion based on your long-term goals using ChatGPT. The tool randomly selects a goal from your goals page and creates a focused, actionable daily task.

## Features

- 🎯 **Random Goal Selection**: Uses RNG to pick different goals each day
- 🤖 **AI-Powered Tasks**: Generates tasks using ChatGPT for better quality and variety
- 📝 **Notion Integration**: Automatically creates tasks in your daily todo database
- 🔌 **Automation Ready**: Can be scheduled to run daily using Windows Task Scheduler
- 🔧 **Detailed Logging**: Comprehensive debug output to track the entire process

## How It Works

1. **Read Goals**: Connects to your Notion workspace and reads a specific page containing your long-term goals
2. **Extract Tasks**: Parses the content to identify individual tasks and goals
3. **Random Selection**: Uses a random number generator to select one goal for the day
4. **AI Generation**: Sends the selected goal to ChatGPT to generate a focused, actionable daily task
5. **Create Task**: Adds the generated task to your Notion database with proper properties

## Prerequisites

- Python 3.7+
- Notion workspace with API access
- OpenAI API key
- A page containing your long-term goals
- A database for daily tasks

## Installation

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd Notion-Random-Task
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up configuration**:
   - Copy `.env.example` to `.env` (if you have one)
   - Update `config.py` with your actual values

## Configuration

Update `config.py` with your actual values:

```python
# Your Notion IDs (replace with your actual IDs)
GOALS_PAGE_ID = "your-actual-goals-page-id-here"
TODO_DATABASE_ID = "your-actual-todo-database-id-here"
```

### Required Values

- **NOTION_TOKEN**: Your Notion integration token
- **OPENAI_API_KEY**: Your OpenAI API key
- **GOALS_PAGE_ID**: ID of the page containing your long-term goals
- **TODO_DATABASE_ID**: ID of your daily todo database

### How to Find Notion IDs

1. **Page ID**: Open the page in Notion, copy the URL, and extract the ID from the end
2. **Database ID**: Open the database, copy the URL, and extract the ID from the end

Example URLs:
- Page: `https://notion.so/My-Goals-1234567890abcdef1234567890abcdef`
- Database: `https://notion.so/My-Todo-Database-abcdef1234567890abcdef1234567890`

## Project Structure

```
Notion-Random-Task/
├── update_database.py    # Main script with NotionTaskGenerator class
├── config.py            # Configuration and environment variables
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## How the Script Works

### 1. Goals Page Reading
- Connects to your Notion workspace using the API
- Reads the specified goals page
- Extracts all content blocks (paragraphs, headings, lists, etc.)

### 2. Task Extraction
- Parses the content to identify individual tasks
- Removes formatting and headers
- Creates a clean list of actionable goals

### 3. Random Selection
- Uses Python's `random.choice()` to select one goal
- Ensures variety in your daily tasks
- Logs which goal was selected

### 4. AI Task Generation
- Sends the selected goal to ChatGPT
- Generates a specific, actionable daily task
- Ensures the task can be completed in 15 minutes

### 5. Notion Integration
- Automatically detects your database structure
- Creates a new page with the generated task
- Sets appropriate properties (title, date, status, etc.)

## Database Requirements

Your Notion database should have:
- A **title property** (required for the task name)
- Optional **select property** for status
- Optional **date property** for task date

The script automatically adapts to your database structure.

## Troubleshooting

### Common Issues

1. **"Name is not a property" Error**
   - The script automatically detects your database properties
   - Make sure your database has at least one property

2. **Empty Goals Content**
   - Check that your goals page has actual content
   - Verify the page ID is correct

3. **OpenAI API Errors**
   - Verify your API key is correct
   - Check your OpenAI account has credits

4. **Notion Permission Errors**
   - Ensure your integration has access to the page and database
   - Check that the page/database IDs are correct

### Debug Information

The script provides extensive logging:
- 🔧 Initialization details
- 📖 Page reading progress
- 🎯 Task extraction results
- 🎲 Random selection details
- 🤖 ChatGPT interaction logs
- 📝 Task creation details

## Customization

### Modify Task Generation

Edit the prompt in `generate_task_with_chatgpt()` method to change:
- Task complexity
- Time requirements
- Tone and style
- Output format

### Change Scheduling

Modify the timing in your Task Scheduler or create a custom service script for more complex scheduling.

## API Limits
- **Notion API**: 3 requests per second
- **OpenAI API**: Depends on your plan (typically 3 requests per minute for free tier)

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the [MIT License](LICENSE).

