#pragma once
#include "Document.h"
#include "VeryImportantDocument.h"
#include "DatedDocument.h"
using namespace std;

class NuclearCodes : public virtual VeryImportantDocument, public virtual DatedDocument{
	void KABOOOM();
};