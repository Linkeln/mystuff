#include <iostream>
#include "ProtectedDocument.h"


using namespace std; 
void ProtectedDocument::SetProtectedContent(string& NewProtectedContent) {
	this->ProtectedContent = NewProtectedContent;
}
string ProtectedDocument::GetProtectedContent() {
	return this->ProtectedContent;
}
void ProtectedDocument::SetProtectedName(string& NewProtectedName) {
	this->ProtectedName = NewProtectedName;
}
string ProtectedDocument::GetProtectedName() {
	return this->ProtectedName;
}