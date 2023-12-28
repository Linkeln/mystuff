#pragma once
#include <string>
#include "Document.h"
using namespace std;

class PrivateDocument : public Document {
private:
	string PrivateContent;
	string PrivateName;
public:
	void SetPrivateContent(const string& NewPrivateContent);
	string GetPrivateContent();
	void SetPrivateName(const string& NewPrivateName);
	string GetPrivateName();
};