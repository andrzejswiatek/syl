#include "stdafx.h"
#include "ImageProcessor.h"
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <iostream>

using namespace std;
using namespace cv;

void ImageProcessor::Process()
{
	Mat image;
	string fileName = "D:\\Repositories\\GITSYL\\syl\\images\\tasma.jpg";
	image = imread(fileName, IMREAD_COLOR); // Read the file

	if (!image.data) // Check for invalid input
	{
		cout << "Could not open or find the image" << std::endl;
		return;
	}

	namedWindow("Display window", WINDOW_AUTOSIZE | WINDOW_GUI_EXPANDED); // Create a window for display.
	imshow("Display window", image); // Show our image inside it.

	waitKey(0); // Wait for a keystroke in the window
}

