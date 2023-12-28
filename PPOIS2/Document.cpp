#include <iostream>
#include "Document.h"

using namespace std;

void Document::SetName(string& NewName){
	this->name = NewName;
}
string Document::GetName() {
	return this->name;
}
void Document::SetContent(string& NewContent) {
	this->content = NewContent;
}
string Document::GetContent() {
	return this->content;
}