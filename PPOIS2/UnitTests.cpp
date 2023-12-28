#include <cassert>
#include "AbilityToCopy.h"
#include "APersonWhoCanWrite.h"
#include "DatedDocument.h"
#include "Document.h"
#include "NuclearCodes.h"
#include "Person.h"
#include "Printer.h"
#include "PrivateDocument.h"
#include "ProtectedDocument.h"
#include "VeryImportantDocument.h"	
#include <iostream>
using namespace std;

void testDocument() {
    // Тестирование метода SetName и GetName
    Document doc;
    string testName = "My Document";
    doc.SetName(testName);
    assert(doc.GetName() == "My Document");

    // Тестирование метода SetContent и GetContent
    string testContent = "This is the content of my document.";
    doc.SetContent(testContent);
    assert(doc.GetContent() == "This is the content of my document.");

    cout << "Все тесты пройдены успешно!" << endl;
}

void testAbilityToCopy() {
    using namespace AbilityToCopy;
    Document doc;
    string testName = "My Document";
    string testContent = "12345";
    doc.SetContent(testContent);
    doc.SetName(testName);
    Document docCopy = CopyDocument(doc);
    assert(docCopy.GetName() == doc.GetName() + "_copy");
    assert(docCopy.GetContent() == doc.GetContent());

    cout << "Все тесты пройдены успешно!" << endl;
}

void testAbilityToPrint() {
    Document doc;
    APersonWhoCanWrite bob;
    string testName = "My Document";
    string testContent = "12345";
    string AssumedOutput = "\nName of the document: My Document\n12345";
    doc.SetContent(testContent);
    doc.SetName(testName);
    string RealOutput = bob.PrintAllContent(doc);
    assert(RealOutput == AssumedOutput);
    cout << "Все тесты пройдены успешно!" << endl;
}

void testPrivateDocument() {
    // Тестирование метода SetName и GetName
    PrivateDocument doc;
    string testName = "My Document";
    doc.SetPrivateName(testName);
    assert(doc.GetPrivateName() == "My Document");

    // Тестирование метода SetContent и GetContent
    string testContent = "This is the content of my document.";
    doc.SetPrivateContent(testContent);
    assert(doc.GetPrivateContent() == "This is the content of my document.");

    cout << "Все тесты пройдены успешно!" << endl;
}

void testProtectedDocument() {
    // Тестирование метода SetName и GetName
    ProtectedDocument doc;
    string testName = "My Document";
    doc.SetProtectedName(testName);
    assert(doc.GetProtectedName() == "My Document");

    // Тестирование метода SetContent и GetContent
    string testContent = "This is the content of my document.";
    doc.SetProtectedContent(testContent);
    assert(doc.GetProtectedContent() == "This is the content of my document.");

    cout << "Все тесты пройдены успешно!" << endl;
}

int main() {
    setlocale(LC_ALL, "Rus");
    testDocument();
    testAbilityToCopy();
    testAbilityToPrint();
    testPrivateDocument();
    testProtectedDocument();
    return 0;
}