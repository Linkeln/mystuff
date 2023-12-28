#include "Printer.h"
#include <iostream>
using namespace std;

string Printer::PrintAllContent(Document& DocumentToPrint) {
	string Output = "\nName of the document: " + DocumentToPrint.GetName() + "\n" + DocumentToPrint.GetContent();
	return Output;
};