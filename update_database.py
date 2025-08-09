import os
import requests
import json
import random
from datetime import datetime
from typing import List, Dict, Any
from openai import OpenAI
from config import NOTION_TOKEN, OPENAI_API_KEY, GOALS_PAGE_ID, TODO_DATABASE_ID

class NotionTaskGenerator:
    def __init__(self, notion_token: str, openai_api_key: str):
        """
        Initialize the NotionTaskGenerator with API keys.
        
        Args:
            notion_token: Your Notion integration token
            openai_api_key: Your OpenAI API key
        """
        print(f"🔧 Initializing NotionTaskGenerator...")
        print(f"   Notion token length: {len(notion_token) if notion_token else 0} characters")
        print(f"   OpenAI API key length: {len(openai_api_key) if openai_api_key else 0} characters")
        
        self.notion_token = notion_token
        self.openai_api_key = openai_api_key
        self.notion_headers = {
            "Authorization": f"Bearer {notion_token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        
        print(f"   Notion headers: {self.notion_headers}")
        
        # Initialize OpenAI client with new API
        self.openai_client = OpenAI(api_key=openai_api_key)
        print(f"   OpenAI client initialized successfully")
        
        # Initialize random number generator
        random.seed()
        print(f"   Random number generator initialized")
        
    def read_goals_page(self, page_id: str) -> Dict[str, Any]:
        """
        Read the content of a specific Notion page containing goals.
        
        Args:
            page_id: The ID of the page containing your long-term goals
            
        Returns:
            Dictionary containing the page content
        """
        print(f"📖 Reading goals page with ID: {page_id}")
        url = f"https://api.notion.com/v1/pages/{page_id}"
        print(f"   Request URL: {url}")
        
        response = requests.get(url, headers=self.notion_headers)
        print(f"   Response status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"   ❌ Error response: {response.text}")
            raise Exception(f"Failed to read page: {response.status_code} - {response.text}")
        
        page_data = response.json()
        print(f"   ✅ Page read successfully")
        print(f"   Page object type: {page_data.get('object', 'unknown')}")
        print(f"   Page title: {page_data.get('properties', {}).get('title', {}).get('title', [{}])[0].get('plain_text', 'No title')}")
            
        return page_data
    
    def get_page_content(self, page_id: str) -> str:
        """
        Extract readable content from a Notion page.
        
        Args:
            page_id: The ID of the page
            
        Returns:
            String containing the page content
        """
        print(f"📖 Extracting content from page: {page_id}")
        
        # First get the page
        page_data = self.read_goals_page(page_id)
        print(f"   Page data keys: {list(page_data.keys())}")
        
        # Get the page content (blocks)
        url = f"https://api.notion.com/v1/blocks/{page_id}/children"
        print(f"   Requesting blocks from: {url}")
        
        response = requests.get(url, headers=self.notion_headers)
        print(f"   Blocks response status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"   ❌ Error getting blocks: {response.text}")
            raise Exception(f"Failed to get page blocks: {response.status_code} - {response.text}")
            
        blocks_data = response.json()
        blocks = blocks_data["results"]
        print(f"   Number of blocks found: {len(blocks)}")
        print(f"   Blocks data keys: {list(blocks_data.keys())}")
        
        # Extract text content from blocks
        content = []
        print(f"   Processing {len(blocks)} blocks...")
        
        for i, block in enumerate(blocks):
            block_type = block.get('type', 'unknown')
            print(f"     Block {i}: {block_type}")
            
            if block_type == "paragraph":
                text_content = block["paragraph"]["rich_text"]
                if text_content:
                    text = "".join([text["plain_text"] for text in text_content])
                    content.append(text)
                    print(f"       Paragraph text: {text[:50]}...")
            elif block_type == "heading_1":
                text_content = block["heading_1"]["rich_text"]
                if text_content:
                    text = "# " + "".join([text["plain_text"] for text in text_content])
                    content.append(text)
                    print(f"       H1 text: {text[:50]}...")
            elif block_type == "heading_2":
                text_content = block["heading_2"]["rich_text"]
                if text_content:
                    text = "## " + "".join([text["plain_text"] for text in text_content])
                    content.append(text)
                    print(f"       H2 text: {text[:50]}...")
            elif block_type == "heading_3":
                text_content = block["heading_3"]["rich_text"]
                if text_content:
                    text = "### " + "".join([text["plain_text"] for text in text_content])
                    content.append(text)
                    print(f"       H3 text: {text[:50]}...")
            elif block_type == "bulleted_list_item":
                text_content = block["bulleted_list_item"]["rich_text"]
                if text_content:
                    text = "- " + "".join([text["plain_text"] for text in text_content])
                    content.append(text)
                    print(f"       Bullet text: {text[:50]}...")
            elif block_type == "numbered_list_item":
                text_content = block["numbered_list_item"]["rich_text"]
                if text_content:
                    text = "1. " + "".join([text["plain_text"] for text in text_content])
                    content.append(text)
                    print(f"       Numbered text: {text[:50]}...")
            elif block_type == "to_do":
                text_content = block["to_do"]["rich_text"]
                if text_content:
                    text = "☐ " + "".join([text["plain_text"] for text in text_content])
                    content.append(text)
                    print(f"       Todo text: {text[:50]}...")
            elif block_type == "toggle":
                text_content = block["toggle"]["rich_text"]
                if text_content:
                    text = "▼ " + "".join([text["plain_text"] for text in text_content])
                    content.append(text)
                    print(f"       Toggle text: {text[:50]}...")
            else:
                print(f"       ⚠️  Unhandled block type: {block_type}")
                print(f"       Block structure: {json.dumps(block, indent=2)[:200]}...")
        
        final_content = "\n".join(content)
        print(f"   Final content length: {len(final_content)} characters")
        print(f"   Content preview: {final_content[:500]}...")
        
        return final_content
    
    def extract_individual_tasks(self, goals_content: str) -> List[str]:
        """
        Extract individual tasks from the goals content and return them as a list.
        
        Args:
            goals_content: The full content of the goals page
            
        Returns:
            List of individual tasks
        """
        print(f"🎯 Extracting individual tasks from goals content...")
        
        # Split content into lines and filter out empty ones
        lines = [line.strip() for line in goals_content.split('\n') if line.strip()]
        print(f"   Total lines found: {len(lines)}")
        
        # Filter lines that look like tasks (remove headers, empty lines, etc.)
        tasks = []
        for i, line in enumerate(lines):
            # Skip lines that are just headers or formatting
            if (line.startswith('#') or 
                line.startswith('##') or 
                line.startswith('###') or
                len(line) < 5 or
                line in ['', ' ', '-', '*']):
                continue
            
            # Clean up the line
            clean_line = line.strip()
            if clean_line.startswith('- '):
                clean_line = clean_line[2:]  # Remove bullet point
            elif clean_line.startswith('1. '):
                clean_line = clean_line[3:]  # Remove numbered point
            elif clean_line.startswith('☐ '):
                clean_line = clean_line[2:]  # Remove todo checkbox
            
            if clean_line and len(clean_line) > 5:
                tasks.append(clean_line)
                print(f"     Task {len(tasks)}: {clean_line[:60]}...")
        
        print(f"   ✅ Extracted {len(tasks)} individual tasks: {tasks}")
        return tasks
    
    def select_random_task(self, tasks: List[str]) -> str:
        """
        Use RNG to select a random task from the list.
        
        Args:
            tasks: List of available tasks
            
        Returns:
            The randomly selected task
        """
        if not tasks:
            print(f"   ⚠️  No tasks available for random selection")
            return "Review and update your goals"
        
        # Use random.choice for selection
        selected_task = random.choice(tasks)
        selected_index = tasks.index(selected_task)
        
        print(f"   🎲 Random number generator selected task {selected_index + 1} out of {len(tasks)}")
        print(f"   🎯 Selected task: {selected_task}")
        
        return selected_task
    
    def get_database_properties(self, database_id: str) -> Dict[str, Any]:
        """
        Get the properties of a database to understand its structure.
        
        Args:
            database_id: The ID of the database
            
        Returns:
            Dictionary containing database properties
        """
        print(f"🗄️  Getting database properties for: {database_id}")
        url = f"https://api.notion.com/v1/databases/{database_id}"
        print(f"   Request URL: {url}")
        
        response = requests.get(url, headers=self.notion_headers)
        print(f"   Response status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"   ❌ Error response: {response.text}")
            raise Exception(f"Failed to get database: {response.status_code} - {response.text}")
            
        database = response.json()
        print(f"   ✅ Database retrieved successfully")
        print(f"   Database title: {database.get('title', [{}])[0].get('plain_text', 'No title')}")
        
        properties = database.get("properties", {})
        print(f"   Number of properties: {len(properties)}")
        
        print("   Available database properties:")
        for prop_name, prop_details in properties.items():
            prop_type = prop_details.get("type", "unknown")
            print(f"     - {prop_name}: {prop_type}")
            if prop_type == "select":
                options = prop_details.get("select", {}).get("options", [])
                print(f"       Select options: {[opt['name'] for opt in options]}")
            elif prop_type == "date":
                print(f"       Date format: {prop_details.get('date', {}).get('format', 'default')}")
            
        return properties
    
    def generate_task_with_chatgpt(self, selected_task: str) -> Dict[str, str]:
        """
        Use ChatGPT to generate a small, actionable task based on the selected goal.
        
        Args:
            selected_task: The randomly selected task from goals
            
        Returns:
            Dictionary with 'title' and 'description' for the new task
        """
        print(f"🤖 Generating task with ChatGPT based on selected goal...")
        print(f"   Selected goal: {selected_task}")
        
        prompt = f"""
        Based on this specific goal, generate ONE small, actionable daily task that would help progress toward it.
        
        Selected Goal:
        {selected_task}
        
        The task should be detailed and specific, and something that can be done within 15 minutes. The tone should be friendly and engaging.
        
        For example, if the goal is to "Learn to code", a task could be "Work on a leetcode challenge!"
        
        Please generate:
        1. A concise, actionable task title (max 6 words, avoid using "Today" or "Daily" or "For X minutes")
        2. A brief description explaining how to accomplish this task (max 2 sentences, do not use "Today" or "Daily" or "For X minutes")
        
        Format your response as JSON:
        {{
            "title": "task title here",
            "description": "description here"
        }}
        """
        
        print(f"   Sending prompt to ChatGPT...")
        print(f"   Prompt length: {len(prompt)} characters")
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that generates actionable daily tasks based on long-term goals."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=256,
                temperature=0.7
            )
            
            print(f"   ✅ ChatGPT response received")
            print(f"   Response object: {type(response)}")
            
            # Extract the response content
            response_text = response.choices[0].message.content.strip()
            print(f"   Raw ChatGPT response: {response_text}")
            
            # Try to parse JSON response
            try:
                # Remove any markdown formatting if present
                if response_text.startswith("```json"):
                    response_text = response_text.split("```json")[1].split("```")[0].strip()
                    print(f"   Cleaned JSON response: {response_text}")
                elif response_text.startswith("```"):
                    response_text = response_text.split("```")[1].split("```")[0].strip()
                    print(f"   Cleaned response: {response_text}")
                
                task_data = json.loads(response_text)
                print(f"   ✅ JSON parsed successfully: {task_data}")
                
                result = {
                    "title": task_data.get("title", "Daily Task"),
                    "description": task_data.get("description", "Task related to your goals")
                }
                print(f"   Final task data: {result}")
                return result
                
            except json.JSONDecodeError as e:
                print(f"   ⚠️  JSON parsing failed: {e}")
                # Fallback if JSON parsing fails
                lines = response_text.split('\n')
                title = "Daily Task"
                description = "Task related to your goals"
                
                for line in lines:
                    if "title" in line.lower():
                        title = line.split(":")[-1].strip().strip('"')
                    elif "description" in line.lower():
                        description = line.split(":")[-1].strip().strip('"')
                
                result = {"title": title, "description": description}
                print(f"   Fallback task data: {result}")
                return result
                
        except Exception as e:
            print(f"   ❌ Error generating task with ChatGPT: {e}")
            print(f"   Error type: {type(e)}")
            return {
                "title": "Daily Task",
                "description": "Task related to your goals"
            }
    
    def create_task_page(self, database_id: str, task_data: Dict[str, str]) -> str:
        """
        Create a new task page in the specified database.
        
        Args:
            database_id: The ID of your daily todo database
            task_data: Dictionary containing 'title' and 'description'
            
        Returns:
            The ID of the created page
        """
        print(f"📝 Creating task page in database: {database_id}")
        print(f"   Task data: {task_data}")
        
        # First, get the database properties to understand its structure
        properties = self.get_database_properties(database_id)
        
        # Find the title property (it's usually the first property or has type "title")
        title_property = None
        for prop_name, prop_details in properties.items():
            if prop_details.get("type") == "title":
                title_property = prop_name
                break
        
        if not title_property:
            # If no title property found, use the first property
            title_property = list(properties.keys())[0]
            print(f"   ⚠️  Warning: No title property found, using '{title_property}' instead")
        else:
            print(f"   ✅ Found title property: {title_property}")
        
        url = "https://api.notion.com/v1/pages"
        print(f"   Request URL: {url}")
        
        # Get today's date
        today = datetime.now().strftime("%Y-%m-%d")
        print(f"   Today's date: {today}")
        
        # Build the properties payload based on what's available
        properties_payload = {
            title_property: {
                "title": [
                    {
                        "text": {
                            "content": task_data["title"]
                        }
                    }
                ]
            }
        }
        
        print(f"   Base properties payload: {json.dumps(properties_payload, indent=2)}")
        
        # Try to add common properties if they exist
        for prop_name, prop_details in properties.items():
            if prop_name == title_property:
                continue
            elif prop_details.get("type") == "select":
                # Add a default status if it's a select property
                options = prop_details.get("select", {}).get("options", [])
                if options:
                    properties_payload[prop_name] = {
                        "select": {"name": options[0]["name"]}
                    }
                    print(f"   Added select property '{prop_name}': {options[0]['name']}")
            elif prop_details.get("type") == "date":
                # Add today's date if it's a date property
                properties_payload[prop_name] = {
                    "date": {"start": today}
                }
                print(f"   Added date property '{prop_name}': {today}")
        
        print(f"   Final properties payload: {json.dumps(properties_payload, indent=2)}")
        
        payload = {
            "parent": {"database_id": database_id},
            "properties": properties_payload,
            "children": [
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": task_data["description"]
                                }
                            }
                        ]
                    }
                }
            ]
        }
        
        print(f"   Full payload: {json.dumps(payload, indent=2)}")
        
        response = requests.post(url, headers=self.notion_headers, json=payload)
        print(f"   Response status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"   ❌ Error response: {response.text}")
            raise Exception(f"Failed to create task: {response.status_code} - {response.text}")
        
        response_data = response.json()
        print(f"   ✅ Task created successfully")
        print(f"   Response data: {json.dumps(response_data, indent=2)}")
        
        task_id = response_data["id"]
        print(f"   Task ID: {task_id}")
        
        return task_id
    
    def generate_daily_task(self, goals_page_id: str, todo_database_id: str) -> str:
        """
        Main method to generate and create a daily task.
        
        Args:
            goals_page_id: ID of the page containing your long-term goals
            todo_database_id: ID of your daily todo database
            
        Returns:
            The ID of the created task page
        """
        print(f"🚀 Starting daily task generation process...")
        print(f"   Goals page ID: {goals_page_id}")
        print(f"   Todo database ID: {todo_database_id}")
        
        print(f"\n📖 Step 1: Reading goals page...")
        goals_content = self.get_page_content(goals_page_id)
        print(f"   ✅ Goals content extracted")
        print(f"   Content length: {len(goals_content)} characters")
        print(f"   Content preview: {goals_content[:500]}...")
        
        print(f"\n🎲 Step 2: Extracting individual tasks...")
        individual_tasks = self.extract_individual_tasks(goals_content)
        
        print(f"\n🎲 Step 3: Randomly selecting a task...")
        selected_task = self.select_random_task(individual_tasks)
        
        print(f"\n📝 Step 4: Generating task with ChatGPT...")
        task_data = self.generate_task_with_chatgpt(selected_task)
        print(f"   ✅ Task generated successfully")
        print(f"   Task title: {task_data['title']}")
        print(f"   Task description: {task_data['description']}")
        
        print(f"\n📝 Step 5: Creating task in Notion...")
        task_id = self.create_task_page(todo_database_id, task_data)
        print(f"   ✅ Task created successfully")
        print(f"   Task ID: {task_id}")
        
        return task_id

def main():
    """
    Main function to run the task generator.
    """
    print(f"🚀 Notion Random Task Generator")
    print(f"================================")
    
    # Check if config values are available
    print(f"\n🔧 Checking configuration...")
    print(f"   NOTION_TOKEN: {'✅ Set' if NOTION_TOKEN else '❌ Missing'}")
    print(f"   OPENAI_API_KEY: {'✅ Set' if OPENAI_API_KEY else '❌ Missing'}")
    print(f"   GOALS_PAGE_ID: {'✅ Set' if GOALS_PAGE_ID and GOALS_PAGE_ID != 'your-goals-page-id-here' else '❌ Missing or default'}")
    print(f"   TODO_DATABASE_ID: {'✅ Set' if TODO_DATABASE_ID and TODO_DATABASE_ID != 'your-todo-database-id-here' else '❌ Missing or default'}")
    
    if not NOTION_TOKEN or not OPENAI_API_KEY:
        print(f"\n❌ Please set NOTION_TOKEN and OPENAI_API_KEY in config.py or as environment variables")
        return
    
    if not GOALS_PAGE_ID or GOALS_PAGE_ID == "your-goals-page-id-here":
        print(f"\n❌ Please set GOALS_PAGE_ID in config.py")
        return
        
    if not TODO_DATABASE_ID or TODO_DATABASE_ID == "your-todo-database-id-here":
        print(f"\n❌ Please set TODO_DATABASE_ID in config.py")
        return
    
    print(f"\n✅ Configuration looks good!")
    
    # Initialize the generator
    print(f"\n🔧 Initializing generator...")
    generator = NotionTaskGenerator(NOTION_TOKEN, OPENAI_API_KEY)
    
    try:
        # Generate and create a daily task
        print(f"\n🚀 Starting task generation...")
        task_id = generator.generate_daily_task(GOALS_PAGE_ID, TODO_DATABASE_ID)
        
        print(f"\n✅ SUCCESS!")
        print(f"   Task ID: {task_id}")
        print(f"   You can view the task in your Notion workspace")
        
    except Exception as e:
        print(f"\n💥 ERROR: {e}")
        print(f"   Error type: {type(e)}")
        import traceback
        print(f"   Full traceback:")
        traceback.print_exc()

if __name__ == "__main__":
    main()
