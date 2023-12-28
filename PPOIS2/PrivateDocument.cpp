#include <iostream>
#include "PrivateDocument.h"


using namespace std;
void PrivateDocument::SetPrivateContent(const string& NewPrivateContent) {
	this->PrivateContent = NewPrivateContent;
}
string PrivateDocument::GetPrivateContent() {
	return this->PrivateContent;
}
void PrivateDocument::SetPrivateName(const string& NewPrivateName) {
	this->PrivateName = NewPrivateName;
}
string PrivateDocument::GetPrivateName() {
	return this->PrivateName;
}