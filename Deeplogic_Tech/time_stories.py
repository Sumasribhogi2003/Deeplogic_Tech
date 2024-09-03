import http.server
import json
import requests
from bs4 import BeautifulSoup

# Function to fetch the HTML content from Time.com
def fetch_html():
    try:
        response = requests.get("https://time.com/")
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.text
    except Exception as e:
        print(f"Error fetching HTML: {e}")
        return ""

# Function to extract the latest 6 stories from the HTML content
def extract_stories(html_content, num_stories=6):
    stories = []
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all article titles and links
    for article in soup.find_all('a', href=True):
        title = article.get_text(strip=True)
        link = article['href']
        if link.startswith('/'):
            link = "https://time.com" + link  # Construct the full URL

        if title and link:
            stories.append({"title": title, "link": link})
        
        if len(stories) >= num_stories:
            break

    return stories

# Handler for HTTP requests
class TimeStoriesHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/getTimeStories':
            html_content = fetch_html()
            stories = extract_stories(html_content, num_stories=6)
            json_response = json.dumps(stories)

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json_response.encode())
        else:
            self.send_response(404)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Not Found")

# Main server setup
if __name__ == '__main__':
    server = http.server.HTTPServer(('localhost', 8080), TimeStoriesHandler)
    print("Server started at http://localhost:8080")
    server.serve_forever()
