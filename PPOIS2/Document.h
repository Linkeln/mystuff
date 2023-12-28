#pragma once
#include <string>
using namespace std;

class Document {
public:
    string name;
    string content;
    void SetName(string& newTitle);
    string GetName();
    virtual void SetContent(string& newContent);
    virtual string GetContent();
};