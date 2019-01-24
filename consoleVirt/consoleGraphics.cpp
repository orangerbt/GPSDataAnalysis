#include <iostream>

#include "consoleGraphics.h"

using namespace std;

consoleGraphics::consoleGraphics()
{
	rootObject = new winObject(&idList); // create root object
	rootObject->id = 0;
	rootObject->title = "0";
	rootObject->topLeft.widthRatio = 0;
	rootObject->topLeft.heightRatio = 0;
	rootObject->botRight.widthRatio = 1;
	rootObject->botRight.heightRatio = 1;

	rootObject->parent = nullptr; // root has no parent
	rootObject->children  = nullptr;
	rootObject->content = nullptr;
	rootObject->lastContentID = 0;
	lastID = 0;

	pair<int, winObject*> newObj(0, rootObject);
	idList.insert(newObj); // add element to idList

}

consoleGraphics::~consoleGraphics()
{
	delete rootObject; // cascade delete everything
}

void consoleGraphics::setHeight(int chars)
{
	windowHeight = chars;
}

void consoleGraphics::setWidth(int chars)
{
	windowWidth = chars;
}

int consoleGraphics::newWinObj(int idParent, bindPoint topLeft, bindPoint botRight)
{
	winObject* tempObjPtr = getObjFromID(idParent);
	if(tempObjPtr == nullptr)
		return(-1);

	return(newWinObj(tempObjPtr,topLeft, botRight));
}

int consoleGraphics::newWinObj(winObject* parent, bindPoint topLeft, bindPoint botRight)
{
	if(parent == nullptr)
		return(-1);

	winObject* curObject = new winObject(&idList); // create new object

	winList* tempChild = parent->children;
	if(tempChild == nullptr) // no children
	{
		parent->children = new winList; // initialize new child
		parent->children->child = curObject;
		parent->children->next = nullptr;
	}
	else
	{
		while(tempChild->next != nullptr)
		{
			tempChild = tempChild->next;
		}
		// tempChild is the last created child

		tempChild->next = new winList; // initialize new child
		tempChild->next->child = curObject;
		tempChild->next->next = nullptr;
	}

	// curObject has been placed in parents child list
	// initialize curObject
	lastID++;
	curObject->id = lastID;
	curObject->title = to_string(lastID);

	curObject->topLeft.widthRatio = topLeft.widthRatio;
	curObject->topLeft.heightRatio = topLeft.heightRatio;
	curObject->botRight.widthRatio = botRight.widthRatio;
	curObject->botRight.heightRatio = botRight.heightRatio;

	curObject->parent = parent;
	curObject->children  = nullptr;
	curObject->content = nullptr;
	curObject->lastContentID = 0;

	pair<int, winObject*> newObj(curObject->id, curObject);
	idList.insert(newObj); // add element to idList

	return(curObject->id);
}

int consoleGraphics::delWinObj(int idParent)
{
	winObject* tempObjPtr = getObjFromID(idParent);
	if(tempObjPtr == nullptr)
		return(-1);

	return(delWinObj(tempObjPtr));
}

int consoleGraphics::delWinObj(winObject* parent)
{
	if(parent == nullptr)
		return(-1);

	delete parent; // cascade deletes children
}

int consoleGraphics::setWindowTitle(int windowID, string title)
{
	winObject* tempObjPtr = getObjFromID(windowID);
	if(tempObjPtr == nullptr)
		return(-1);

	return(setWindowTitle(tempObjPtr, title));
}

int consoleGraphics::setWindowTitle(winObject* window, string title)
{
	if(window == nullptr)
		return(-1);

	window->title = title;
	return(0);
}

void* consoleGraphics::newWinContent(int windowID, int location, int contentType)
{
	winObject* tempObjPtr = getObjFromID(windowID);
	if(tempObjPtr == nullptr)
		return(nullptr);

	return(newWinContent(tempObjPtr, location, contentType));
}

void* consoleGraphics::newWinContent(winObject* window, int location, int contentType)
{
	// adds content of specified type to window.
	// returns pointer to content data.
	// places new content at index specified by location, or end of list. Whichever comes first. -1 is always end of list.
	if(window == nullptr)
		return(nullptr);

	if(window->content == nullptr || location == 0) // check if content Exists
	{
		winContent* tempContentPtr = window->content;

		window->content = new winContent;
		window->content->next = tempContentPtr;
		window->content->contentType = contentType;

		switch(contentType)
		{
		case(TEXT_CONTENT):
			window->content->data = new textContent;
			break;
		case(GRAPH_CONTENT):
			break;
		case(BAR_CONTENT):
			window->content->data = new barContent;
			break;
		}
		window->content->contentID = window->lastContentID;
		window->lastContentID++;
		return(window->content->data);
	}
	int curIndex = 0;
	winContent* curContentPtr = window->content;
	while((curIndex < location || location == -1) && curContentPtr->next != nullptr)
	{
		curContentPtr = curContentPtr->next;
	}

	winContent* tempContentPtr = curContentPtr->next;
	curContentPtr->next = new winContent;
	curContentPtr->next->next = tempContentPtr;
	curContentPtr->next->contentType = contentType;
	switch(contentType)
	{
	case(TEXT_CONTENT):
		curContentPtr->next->data = new textContent;
		break;
	case(GRAPH_CONTENT):
		break;
	case(BAR_CONTENT):
		curContentPtr->next->data = new barContent;
		break;
	}

	window->lastContentID++;

	return(curContentPtr->next->data);
}


consoleGraphics::winObject* consoleGraphics::getObjFromID(int id)
{
	if(idList.count(id) == 0)
		return(nullptr);

	return(idList[id]);
}

void consoleGraphics::printObjects(winObject* obj)
{
	if(obj->children != nullptr)
	{
		winList* curChild = obj->children;
		while(curChild != nullptr)
		{
			printObjects(curChild->child);
			curChild = curChild->next;
		}
	}

	cout << "Object: " << obj->id << " Top Left: (" << obj->topLeft.widthRatio << "," << obj->topLeft.heightRatio << ") Bot Right: ("
	     << obj->botRight.widthRatio << "," << obj->botRight.heightRatio << ")" << endl;
}

void consoleGraphics::draw()
{
	cout << "\0337";
	//cout << "\033[2JH";
	cout << "\033[2J";
	drawObject(rootObject, 1, 1, windowHeight, windowWidth);
	cout << "\0338" << flush;
}

void consoleGraphics::drawContent(int windowID, bool saveCursor)
{
	winObject* tempObjPtr = getObjFromID(windowID);
	if(tempObjPtr == nullptr)
		return;

	drawContent(tempObjPtr, saveCursor);
}

void consoleGraphics::drawContent(winObject* obj, bool saveCursor)
{
	if(saveCursor)
		cout << "\0337";

	winContent* curContent = obj->content;
	int curY = obj->top + 1;

	while(curContent != nullptr) // print all content
	{
		switch(curContent->contentType)
		{
		case(TEXT_CONTENT):
			curY = drawText(obj, ((textContent*)curContent->data)->text, curY);
			break;
		case(GRAPH_CONTENT):
			break;
		case(BAR_CONTENT):
			curY = drawBar(obj, (barContent*)curContent->data,curY);
			break;
		}

		if(curY >= obj->bot) // stop printing if window is filled
			break;

		curContent = curContent->next;
	}

	while(curY < obj->bot) // erase rest of content
	{
		curY = drawText(obj, "\n", curY); // print new lines until content is cleared
	}

	if(saveCursor)
		cout << "\0338" << flush;
}

int consoleGraphics::drawText(winObject* obj, string text, int curY)
{
	int charCounter = 0;
	bool lineDone = false;
	bool lastCovered = true;

	for(int y = curY ; y < obj->bot; y++)
	{
		for(int x = obj->left + 1; x < obj->right - 1; x++)
		{
			if(lineDone) // erase remaining content if line done
			{
				if(lastCovered)
				{
					// last covered, reset position
					cout << "\033[" << y << ";" << x << "H";
					lastCovered = false;
				}

				if(!checkIfCovered(x, y, obj))
				{
					cout << ' ';
				}
				else
				{
					lastCovered = true;
				}
				continue;
			}

			// check if content is done
			if(text.length() < charCounter)
			{
				lineDone = true; // erase rest of line
				continue;
			}

			char curChar = text[charCounter];

			if(!checkIfCovered(x, y, obj))
			{
				// not covered
				if(lastCovered)
				{
					// last covered, reset position
					cout << "\033[" << y << ";" << x << "H";

				}
				switch(curChar)
				{
				case('\n'):
					lineDone = true;
					cout << ' ';
					break;
				default:
					cout << curChar;
				}
				lastCovered = false;
			}
			else
			{
				// covered, set flag
				lastCovered = true;
			}

			// prints done, increment counter
			charCounter++;
		}
		// check if content is done printing
		if(text.length() < charCounter)
		{
			return(y + 1);
		}
		lineDone = false;
		lastCovered = true;
	}
	return(obj->bot); // reached end of window
}

int consoleGraphics::drawBar(winObject* obj, barContent* barData, int curY)
{

//	if(barData->barWidth < 1)
//		return(-1);

//		std::list<int> barFillPercent;
//		std::list<std::string> barLabel;
//		int barType;
//		int height;
	bool lineDone = false;
	bool graphDone = false;
	bool lastCovered = true;
	int curChar = 0;

	int longestLabel = 0; // find longest label, for correct spacing
	if(barData->topLabel.length() > longestLabel)
		longestLabel = barData->topLabel.length();
	if(barData->midLabel.length() > longestLabel)
		longestLabel = barData->midLabel.length();
	if(barData->botLabel.length() > longestLabel)
		longestLabel = barData->botLabel.length();

	for(int y = curY ; y < obj->bot; y++)
	{
		list<int>::iterator barIt = barData->barFillPercent.begin();
		list<string>::iterator labelIt = barData->barLabel.begin();
		for(int x = obj->left + 1; x < obj->right - 1; x++)
		{
			if(lineDone) // erase remaining content if line done
			{
				if(lastCovered)
				{
					// last covered, reset position
					cout << "\033[" << y << ";" << x << "H";
					lastCovered = false;
				}

				if(!checkIfCovered(x, y, obj))
				{
					cout << ' ';
				}
				else
				{
					lastCovered = true;
				}
				continue;
			}

			if(!checkIfCovered(x, y, obj)) //print bars & labels
			{
				// not covered
				if(lastCovered)
				{
					// last covered, reset position
					cout << "\033[" << y << ";" << x << "H";
					lastCovered = false;
				}

				// print bars & labels
				if(x - obj->left > longestLabel)
				{
					int curXPos = x - obj->left - longestLabel - 1;
					if(y - curY > barData->height - 2)
					{ // check if bars are done

						if(curXPos%(barData->barWidth+1) == 0)
						{
							cout << ' ';
						}
						else
						{
							if((*labelIt).size() < (curXPos%(barData->barWidth+1)))
							{
								cout << ' ';
							}
							else
							{
								cout << (*labelIt)[(curXPos%(barData->barWidth+1))-1];
							}


							if((curXPos+1)%(barData->barWidth+1) == 0)
								labelIt++;
						}
						if(labelIt == barData->barLabel.end())
						{
							lineDone = true;
							graphDone = true;
						}
						continue;
					}

					if(y - curY == 0 || y - curY == barData->height - 2)
					{
						if(barData->barFillPercent.size() * (barData->barWidth+1) < curXPos)
						{
							cout << ' ';
							lineDone = true;
							continue;
						}

						if(curXPos%(barData->barWidth+1) == 0)
						{
							cout << '+';
						}
						else
						{
							cout << '-';
						}
					}
					else if(curXPos%(barData->barWidth+1) == 0)
					{
						cout << '|';
					}
					else
					{
						if(barIt == barData->barFillPercent.end())
						{
							cout << ' ';
							lineDone = true;
							continue;
						}
						if(*barIt < (100/(barData->height - 2)) * ((barData->height - 2) - (y - curY)))
							cout << ' ';
						else
							cout << '#';

						if((curXPos+1)%(barData->barWidth+1) == 0)
							barIt++;
					}
				}
				else if(y - curY == 0)
				{
					if(barData->topLabel.length() > curChar)
						cout << barData->topLabel[curChar];
					else
						cout << ' ';
				}
				else if(y - curY == (barData->height - 2) / 2)
				{
					if(barData->midLabel.length() > curChar)
						cout << barData->midLabel[curChar];
					else
						cout << ' ';
				}
				else if(y - curY == barData->height - 2)
				{
					if(barData->botLabel.length() > curChar)
						cout << barData->botLabel[curChar];
					else
						cout << ' ';
				}
				else
				{
					cout << ' '; // print space for labels
				}
			}
			else
			{
				//covered
				lastCovered = true;
			}
			curChar++;
		}
		if(graphDone == true)
		{
			return(curY + barData->height);
		}
		lineDone = false;
		lastCovered = true;
		curChar = 0;
	}

	return(curY + obj->bot);
}

void consoleGraphics::drawObject(winObject* obj, int topChar, int leftChar, int botChar, int rightChar)
{
	int realTop;
	int realLeft;
	int width;
	int height;

	int parentHeight = botChar - topChar;
	height = (parentHeight * obj->botRight.heightRatio) - (parentHeight * obj->topLeft.heightRatio);

	int parentWidth = rightChar - leftChar;
	width = (parentWidth * obj->botRight.widthRatio) - (parentWidth * obj->topLeft.widthRatio) + 1;

	realTop = (parentHeight * obj->topLeft.heightRatio) + topChar;
	realLeft = (parentWidth * obj->topLeft.widthRatio) + leftChar;

	// set position variables
	obj->top = realTop;
	obj->bot = realTop + height;
	obj->left = realLeft;
	obj->right = realLeft + width;


	cout << "\033[" << realTop << ";" << realLeft + 1 << "H";
	for(int i = 1; i < width -1; i++)
	{
		cout << "-";
	}

	cout << "\033[" << realTop + height << ";" << realLeft + 1 << "H";
	for(int i = 1; i < width -1; i++)
	{
		cout << "-";
	}

	for(int i = 1; i < height; i++)
	{
		cout << "\033[" << realTop + i << ";" << realLeft << "H|";
		for(int j = 0; j < width - 2; j++)
		{
			cout << " ";
		}
		cout << "|";
	}

	cout << "\033[" << realTop << ";" << realLeft << "H+";
	if(obj->title.length() > 0)
		cout << "|" << obj->title << "|";

	cout << "\033[" << realTop << ";" << realLeft + width-1 << "H";
	cout << "+";

	cout << "\033[" << realTop + height << ";" << realLeft << "H";
	cout << "+";

	cout << "\033[" << realTop + height << ";" << realLeft + width -1 << "H";
	cout << "+";

	// draw children on top
	winList* curChild = obj->children;
	while(curChild != nullptr)
	{
		drawObject(curChild->child, realTop, realLeft, realTop + height, realLeft + width);
		curChild = curChild->next;
	}

	// draw content after children are done
	drawContent(obj, false);
}

bool consoleGraphics::checkIfCovered(int x, int y, winObject* curObj)
{

	winList* curList = curObj->children;
	while(curList != nullptr)
	{
		winObject* curObj = curList->child;

		if(curObj->top <= y && curObj->bot >= y &&
		   curObj->left <= x && curObj->right > x)
			return(true); // covered


		curList = curList->next;
	}

	return(false); // not covered
}
