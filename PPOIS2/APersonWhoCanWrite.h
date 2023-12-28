#pragma once
#include "Printer.h"
#include "Person.h"

class APersonWhoCanWrite : public Person, public Printer {
public:
	int WordsPerMinute;
};