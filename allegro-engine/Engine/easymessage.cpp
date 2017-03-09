/*
  ****************************************************************************
  * Copyright (c) 2009, Richard Marks, CCPS Solutions,                       *
  * Undefined Aeon Software.                                                 *
  *                                                                          *
  * Permission is hereby granted, free of charge, to any person obtaining a  *
  * copy of this software and associated documentation files (the            *
  * "Software"), to deal in the Software without restriction, including      *
  * without limitation the rights to use, copy, modify, merge, publish,      *
  * distribute, distribute with modifications, sub-license, and/or sell      *
  * copies of the Software, and to permit persons to whom the Software is    *
  * furnished to do so, subject to the following conditions:                 *
  *                                                                          *
  * The above copyright notice and this permission notice shall be included  *
  * in all copies or substantial portions of the Software.                   *
  *                                                                          *
  * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS  *
  * OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF               *
  * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT.  *
  * IN NO EVENT SHALL THE ABOVE COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,   *
  * DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR    *
  * OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR    *
  * THE USE OR OTHER DEALINGS IN THE SOFTWARE.                               *
  *                                                                          *
  * Except as contained in this notice, the name(s) of the above copyright   *
  * holders shall not be used in advertising or otherwise to promote the     *
  * sale, use or other dealings in this Software without prior written       *
  * authorization.                                                           *
  ****************************************************************************
*/

/*
	How to do a custom message box in Allegro
	a simple utility class by Richard Marks

	supplied below is a simple method for outputting a message to the user in Allegro

	the way it works is you create an instance of the class when you want to show a message

	Example:

	EasyMessage msg("Hello, World!");

*/
#include <allegro.h>
#include "easymessage.h"

#include <vector>

// config
#define EASYMESSAGE_DIALOGBOX_WIDTH						SCREEN_W / 2
#define EASYMESSAGE_DIALOGBOX_HEIGHT					96
#define EASYMESSAGE_DIALOGBOX_TOP_BORDER_WIDTH 			2
#define EASYMESSAGE_DIALOGBOX_BOTTOM_BORDER_WIDTH 		4
#define EASYMESSAGE_DIALOGBOX_LEFT_BORDER_WIDTH 		1
#define EASYMESSAGE_DIALOGBOX_RIGHT_BORDER_WIDTH 		1

// colors
#define EASYMESSAGE_DIALOGBOX_BORDER_COLOR 				makecol(150, 145, 135)
#define EASYMESSAGE_DIALOGBOX_BACKGROUND_COLOR			makecol(193, 189, 181)

#define EASYMESSAGE_DIALOGBOX_MESSAGE_BORDER_COLOR		makecol(150, 145, 135)
#define EASYMESSAGE_DIALOGBOX_MESSAGE_BACKGROUND_COLOR 	makecol(193, 189, 181)
#define EASYMESSAGE_DIALOGBOX_MESSAGE_TEXT_COLOR 		makecol(0, 0, 0)

#define EASYMESSAGE_DIALOGBOX_BUTTON_BORDER_COLOR		makecol(150, 145, 135)
#define EASYMESSAGE_DIALOGBOX_BUTTON_BACKGROUND_COLOR 	makecol(193, 189, 181)
#define EASYMESSAGE_DIALOGBOX_BUTTON_TEXT_COLOR 		makecol(0, 0, 0)

#define EASYMESSAGE_DIALOGBOX_TITLE_BACKGROUND_COLOR	makecol(42, 86, 168)
#define EASYMESSAGE_DIALOGBOX_TITLE_TEXT_COLOR			makecol(172, 184, 200)

std::vector<std::string> string_tokenizer(const std::string& source, const std::string& delimiters)
{
	std::vector<std::string> tokens;
	size_t p0 = 0;
	size_t p1 = std::string::npos;
	while (p0 != std::string::npos)
	{
		p1 = source.find_first_of(delimiters, p0);
		if (p1 != p0)
		{
			std::string token = source.substr(p0, p1 - p0);
			tokens.push_back(token);
		}
		p0 = source.find_first_not_of(delimiters, p1);
	}
	return tokens;
}


EasyMessage::EasyMessage(EasyOptions options, const char* message, const char* title, const char* buttonlabel) :
	dialogbox_(0)
{
	BITMAP* dialogboxbackbuffer;
	BITMAP* rendertarget = screen;

	// the padding between controls
	const int controlpadding = 2;

	// get a few constants for the font dimensions
	const int fontwidth = text_length(font, "A");
	const int fontheight = text_height(font);

	// get some constants for the border
	const int hborderwidth = EASYMESSAGE_DIALOGBOX_LEFT_BORDER_WIDTH + EASYMESSAGE_DIALOGBOX_RIGHT_BORDER_WIDTH;
	const int vborderwidth = EASYMESSAGE_DIALOGBOX_TOP_BORDER_WIDTH + EASYMESSAGE_DIALOGBOX_BOTTOM_BORDER_WIDTH;

	// break the message into lines based on the \n character
	std::string m = message;
	std::vector<std::string> messagelines = string_tokenizer(m, "\n");

	// create the button control
	int bw = (controlpadding * 4) + text_length(font, buttonlabel) + fontwidth * 4;
	int bh = (controlpadding * 8) + fontheight;
	BITMAP* btncontrol = create_bitmap(bw, bh);



	// calculate the size of the dialog box

	// the minimum width of the dialog box is the title length + borders
	const int minboxwidth = hborderwidth + text_length(font, title);

	// the minimum height of the dialog box is the height of the message + borders + button height
	const int minboxheight = fontheight + 4 + (vborderwidth*4) + (messagelines.size()*3) + (fontheight * messagelines.size()) + bh;

	// the maximum width of the dialog box is the width of the screen - 16
	const int maxboxwidth = SCREEN_W - 16;

	// the maximum height of the dialogbox is the height of the screen - 16
	const int maxboxheight = SCREEN_H - 16;

	// calculate the width of the dialog box
	int longestline = 0;
	std::vector<std::string>::iterator iter;
	for (iter = messagelines.begin(); iter != messagelines.end(); iter++)
	{
		int linelen = (int)(*iter).size();
		longestline = (linelen > longestline) ? linelen : longestline;
	}
	int boxwidth = (fontwidth * longestline) + hborderwidth + (controlpadding * 2);
	if (boxwidth < minboxwidth) { boxwidth = minboxwidth; }
	if (boxwidth > maxboxwidth) { boxwidth = maxboxwidth; }

	// calculate the height of the dialogbox
	int boxheight = minboxheight;
	if (boxheight > maxboxheight) { boxheight = maxboxheight; }

	// center the box on the screen
	boxx_ = SCREEN_W / 2 - boxwidth / 2;
	boxy_ = SCREEN_H / 2 - boxheight / 2;

	// create the dialog box
	dialogbox_ = create_bitmap(boxwidth, boxheight);
	dialogboxbackbuffer = create_bitmap(boxwidth, boxheight);
	clear_to_color(dialogbox_, EASYMESSAGE_DIALOGBOX_BORDER_COLOR);

	// draw border on te dialog box
	rectfill(dialogbox_,
		EASYMESSAGE_DIALOGBOX_LEFT_BORDER_WIDTH,
		EASYMESSAGE_DIALOGBOX_TOP_BORDER_WIDTH,
		dialogbox_->w - (EASYMESSAGE_DIALOGBOX_LEFT_BORDER_WIDTH + EASYMESSAGE_DIALOGBOX_RIGHT_BORDER_WIDTH),
		dialogbox_->h - (EASYMESSAGE_DIALOGBOX_TOP_BORDER_WIDTH + EASYMESSAGE_DIALOGBOX_BOTTOM_BORDER_WIDTH),
		EASYMESSAGE_DIALOGBOX_BACKGROUND_COLOR);

	// draw the title background
	rectfill(dialogbox_,
		EASYMESSAGE_DIALOGBOX_LEFT_BORDER_WIDTH + 1,
		EASYMESSAGE_DIALOGBOX_TOP_BORDER_WIDTH + 1,
		dialogbox_->w - (2 + EASYMESSAGE_DIALOGBOX_LEFT_BORDER_WIDTH + EASYMESSAGE_DIALOGBOX_RIGHT_BORDER_WIDTH),
		fontheight+4,
		EASYMESSAGE_DIALOGBOX_TITLE_BACKGROUND_COLOR);

	// draw the title text
	textprintf_ex(dialogbox_, font,
		dialogbox_->w / 2 - (text_length(font, title)/2),
		EASYMESSAGE_DIALOGBOX_TOP_BORDER_WIDTH + 2,
		EASYMESSAGE_DIALOGBOX_TITLE_TEXT_COLOR, -1, "%s", title);

/**

#define EASYMESSAGE_DIALOGBOX_MESSAGE_BORDER_COLOR		makecol(150, 145, 135)
#define EASYMESSAGE_DIALOGBOX_MESSAGE_BACKGROUND_COLOR 	makecol(193, 189, 181)
#define EASYMESSAGE_DIALOGBOX_MESSAGE_TEXT_COLOR 		makecol(0, 0, 0)

#define EASYMESSAGE_DIALOGBOX_BUTTON_BORDER_COLOR		makecol(150, 145, 135)
#define EASYMESSAGE_DIALOGBOX_BUTTON_BACKGROUND_COLOR 	makecol(193, 189, 181)
#define EASYMESSAGE_DIALOGBOX_BUTTON_TEXT_COLOR 		makecol(0, 0, 0)

*/

	// draw the message lines
	switch(options)
	{
		case EasyCentered:
		{
			int cx = dialogbox_->w / 2;
			int printy = fontheight + 4 + vborderwidth;
			for (iter = messagelines.begin(); iter != messagelines.end(); iter++)
			{
				textprintf_ex(dialogbox_, font, cx - (text_length(font, (*iter).c_str())/2),
				printy, EASYMESSAGE_DIALOGBOX_MESSAGE_TEXT_COLOR, -1, "%s", (*iter).c_str());
				printy += (3+fontheight);
			}
		} break;

		case EasyLeft:
		{
			int printy = fontheight + 4 + vborderwidth;
			for (iter = messagelines.begin(); iter != messagelines.end(); iter++)
			{
				textprintf_ex(dialogbox_, font, controlpadding + hborderwidth, printy,
				EASYMESSAGE_DIALOGBOX_MESSAGE_TEXT_COLOR, -1, "%s", (*iter).c_str());
				printy += (3+fontheight);
			}
		} break;

		case EasyRight:
		{
			int printy = fontheight + 4 + vborderwidth;
			for (iter = messagelines.begin(); iter != messagelines.end(); iter++)
			{
				textprintf_ex(dialogbox_, font, dialogbox_->w - (controlpadding + hborderwidth +
				text_length(font, (*iter).c_str())), printy, EASYMESSAGE_DIALOGBOX_MESSAGE_TEXT_COLOR,
				-1, "%s", (*iter).c_str());
				printy += (3+fontheight);
			}
		} break;
		default: break;
	}




	clear_to_color(btncontrol, EASYMESSAGE_DIALOGBOX_BUTTON_BORDER_COLOR);
	rectfill(btncontrol, 1, 1, bw - 2, bh - 2, EASYMESSAGE_DIALOGBOX_BUTTON_BACKGROUND_COLOR);
	int blx = bw / 2 - (text_length(font, buttonlabel) / 2);
	int bly = bh / 2 - (text_height(font) / 2);
	textprintf_ex(btncontrol, font, blx, bly, EASYMESSAGE_DIALOGBOX_BUTTON_TEXT_COLOR, -1, "%s", buttonlabel);

	// position the button at the bottom of the dialog box, centered horizontally
	int bx = dialogbox_->w / 2 - bw / 2;
	int by = dialogbox_->h - (EASYMESSAGE_DIALOGBOX_BOTTOM_BORDER_WIDTH + bh + (4 * controlpadding));

	// draw the button control on the dialog box
	blit(btncontrol,dialogbox_,0,0,bx,by,btncontrol->w,btncontrol->h);
	if (btncontrol){destroy_bitmap(btncontrol);}




	clear_keybuf();
	bool closedialogbox = false;
	while(!closedialogbox)
	{
		if (key[KEY_ESC] || key[KEY_ENTER])
		{
			closedialogbox = true;
		}
		if (!this->update())
		{
			closedialogbox = true;
		}
		this->render(dialogboxbackbuffer);
		rest(10);
		blit(dialogboxbackbuffer, rendertarget, 0, 0, boxx_, boxy_, dialogboxbackbuffer->w, dialogboxbackbuffer->h);
	}
	clear_keybuf();

	if (dialogbox_)
	{
		destroy_bitmap(dialogbox_);
	}

	if (dialogboxbackbuffer)
	{
		destroy_bitmap(dialogboxbackbuffer);
	}
}

EasyMessage::~EasyMessage(){}

bool EasyMessage::update()
{
	// handle any key press to close
	/*
	while(keypressed())
	{
		int k = readkey();
		char scancode = k >> 8;
		switch(scancode)
		{
			default: { return false; } break;
		}
	}
	*/
	return true;
}

void EasyMessage::render(BITMAP* buffer)
{
	// blit our dialog box gui image
	blit(dialogbox_, buffer, 0, 0, 0, 0, dialogbox_->w, dialogbox_->h);
}
