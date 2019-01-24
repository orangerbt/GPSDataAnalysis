
#include <iostream>
#include <sys/ioctl.h>
#include <unistd.h>
#include <stdlib.h>
#include <time.h>
#include <string>

#include "consoleGraphics.h"

using namespace std;

int main()
{
	srand (time(NULL));
	consoleGraphics cGraph;

	struct winsize size;
	ioctl(STDOUT_FILENO,TIOCGWINSZ,&size);

	cGraph.setHeight(size.ws_row - 1);
	cGraph.setWidth(size.ws_col);

	cout << "\033[" << size.ws_row << ";0H";


	cGraph.setWindowTitle(0, "Root");

	int dataWin1 = cGraph.newWinObj(0, consoleGraphics::bindPoint{0.7,0.05}, consoleGraphics::bindPoint{0.9,0.7});
	cGraph.setWindowTitle(dataWin1, "Data");

	int botRightWin = cGraph.newWinObj(0, consoleGraphics::bindPoint{0.7,0.7}, consoleGraphics::bindPoint{0.9,0.9});
	int tempWin = cGraph.newWinObj(0, consoleGraphics::bindPoint{0.02,0.05}, consoleGraphics::bindPoint{0.7,0.7});
	int childWin = cGraph.newWinObj(tempWin, consoleGraphics::bindPoint{0.4,0.15}, consoleGraphics::bindPoint{0.9,0.9});

	cGraph.setWindowTitle(botRightWin, "BotRight");

	consoleGraphics::textContent* tempContent = (consoleGraphics::textContent*)cGraph.newWinContent(childWin, -1, TEXT_CONTENT);
	tempContent->text = "Test";

	cGraph.setWindowTitle(tempWin, "Text");
	consoleGraphics::textContent* randomContent = (consoleGraphics::textContent*)cGraph.newWinContent(tempWin, -1, TEXT_CONTENT);
	consoleGraphics::textContent* longContent = (consoleGraphics::textContent*)cGraph.newWinContent(tempWin, -1, TEXT_CONTENT);

	longContent->text = "Helo World!\nI am long text that goes on forever and ever";
	for(int i = 0; i < 50; i++)
		longContent->text.append(" and ever");


	cGraph.setWindowTitle(childWin, "");
	consoleGraphics::textContent* childContent = (consoleGraphics::textContent*)cGraph.newWinContent(childWin, -1, TEXT_CONTENT);
	consoleGraphics::barContent* childBar = (consoleGraphics::barContent*)cGraph.newWinContent(childWin, -1, BAR_CONTENT);

	childContent->text = "Child window text!\nNext line\n";

	childBar->topLabel = "100% ";
	childBar->midLabel = "50% ";
	childBar->botLabel = "0% ";
	childBar->barFillPercent.push_back(40);
	childBar->barFillPercent.push_back(30);
	childBar->barFillPercent.push_back(75);
	childBar->barFillPercent.push_back(100);
	childBar->barFillPercent.push_back(0);
	childBar->barFillPercent.push_back(5);
	childBar->barFillPercent.push_back(10);
	childBar->barFillPercent.push_back(15);
	childBar->barFillPercent.push_back(20);
	childBar->barFillPercent.push_back(25);
	childBar->barFillPercent.push_back(30);
	childBar->barFillPercent.push_back(35);
	childBar->barLabel.push_back("A");
	childBar->barLabel.push_back("B");
	childBar->barLabel.push_back("C");
	childBar->barLabel.push_back("D");
	childBar->barLabel.push_back("E");
	childBar->barLabel.push_back("F");
	childBar->barLabel.push_back("G");
	childBar->barLabel.push_back("H");
	childBar->barLabel.push_back("I");
	childBar->barLabel.push_back("J");
	childBar->barLabel.push_back("K");
	childBar->barLabel.push_back("L");
	childBar->barType = 0;
	childBar->height = 12;
	childBar->barWidth = 5;

	cGraph.draw(); // draw windows

	for(int i = 0; i < 20; i++)
	{
		cGraph.drawContent(childWin, true);
		usleep(1000000);
		for(list<int>::iterator it = childBar->barFillPercent.begin(); it!=childBar->barFillPercent.end(); it++)
		{
			(*it) = rand() % 100;
		}
	}



	consoleGraphics::textContent* dataWin1Content = (consoleGraphics::textContent*)cGraph.newWinContent(dataWin1, -1, TEXT_CONTENT);

	dataWin1Content->text = "Temperature: ";

	//cGraph.draw(); // draw windows
	cGraph.drawContent(dataWin1, true);

	string inputString;
	cin >> inputString;

	dataWin1Content->text.append(inputString);
	cGraph.draw(); // draw windows
	//cGraph.drawContent(dataWin1, true);

	cin.ignore(256, ' ');

	return(0);
}
