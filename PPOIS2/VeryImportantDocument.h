#pragma once
// по сути тот же класс что и Document
#include <string>
#include "Document.h"
using namespace std;

class VeryImportantDocument : public virtual Document {
public:
	string Password;
};

