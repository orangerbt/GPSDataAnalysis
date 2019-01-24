
#include <unordered_map>
#include <list>

#define TEXT_CONTENT 0
#define GRAPH_CONTENT 1
#define BAR_CONTENT 2

class consoleGraphics
{
private:
	struct winList;
	struct winContent;
public:
	struct bindPoint;
	struct winObject;

	struct textContent
	{
		std::string text;

		textContent(){text = "";};
	};

	struct barContent
	{
		std::string topLabel;
		std::string midLabel;
		std::string botLabel;
		std::list<int> barFillPercent;
		std::list<std::string> barLabel;
		int barType;
		int height;
		int barWidth;

		barContent()
		{
			topLabel = midLabel = botLabel = "";
			barType = 0;
			height = 5;
			barWidth = 2;
		}
	};

	struct bindPoint
	{
		double widthRatio;
		double heightRatio;
	};

	struct winObject
	{
		int id;
		std::string title;
		// settings
		winContent* content;
		int lastContentID;

		bindPoint topLeft;
		bindPoint botRight;
		winObject* parent;
		winList* children;

		std::unordered_map<int, winObject*>* idListPtr;

		winObject(std::unordered_map<int, winObject*>* idList) {idListPtr = idList;};

		int top;
		int bot;
		int left;
		int right;

		~winObject() // remove all children before removing self
		{
			// remove content
			winContent* curContent = content;
			while(curContent != nullptr)
			{
				winContent* temp = curContent;
				curContent = curContent->next;
				delete temp;
			}

			// remove children
			winList* temp = children;
			while(temp != nullptr)
			{
				delete temp->child;
				winList* delPtr = temp;
				temp = temp->next;
				delete delPtr;
			}
			idListPtr->erase(id);
		}
	};

	consoleGraphics();
	~consoleGraphics();

	void setHeight(int chars);
	void setWidth(int chars);

	int newWinObj(int idParent, bindPoint topLeft, bindPoint botRight);
	int newWinObj(winObject* parent, bindPoint topLeft, bindPoint botRight);

	int delWinObj(int idParent);
	int delWinObj(winObject* parent);

	int setWindowTitle(int windowID, std::string title);
	int setWindowTitle(winObject* window, std::string title);

	void* newWinContent(int windowID, int location, int contentType); // -1 for end of list
	void* newWinContent(winObject* window, int location, int contentType); // -1 for end of list

	winObject* getObjFromID(int id);

	// debug
	void printObjects(winObject* obj);

	void draw();
	void drawContent(int windowID, bool saveCursor);
	void drawContent(winObject* obj, bool saveCursor);

private:
	struct winList
	{
		winObject* child;
		winList* next;
	};

	struct winContent
	{
		int contentType;
		int contentID;
		void* data; // pointer to data content needed
		winContent* next;
	};

	winObject* rootObject;

	int windowHeight;
	int windowWidth;
	int lastID;

	void drawObject(winObject* obj, int topChar, int leftChar, int botChar, int rightChar);

	int drawText(winObject* obj, std::string text, int curY);
	int drawBar(winObject* obj, barContent* barData, int curY);

	bool checkIfCovered(int x, int y, winObject* curObj);

	std::unordered_map<int, winObject*> idList;
};
