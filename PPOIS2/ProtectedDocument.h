#pragma once
#include <string>
#include "Document.h"
using namespace std;

class ProtectedDocument : public Document {
protected:
	string ProtectedContent;
	string ProtectedName;
public:
	void SetProtectedContent(string& NewProtectedContent);
	string GetProtectedContent();
	void SetProtectedName(string& NewProtectedName);
	string GetProtectedName();
};