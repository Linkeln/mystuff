#include "pch.h"
#include "CppUnitTest.h"
#include "../PPOIS 2/AbilityToCopy.h"
#include "../PPOIS 2/APersonWhoCanWrite.h"
#include "../PPOIS 2/DatedDocument.h"
#include "../PPOIS 2/Document.h"
#include "../PPOIS 2/NuclearCodes.h"
#include "../PPOIS 2/Person.h"
#include "../PPOIS 2/Printer.h"
#include "../PPOIS 2/PrivateDocument.h"
#include "../PPOIS 2/ProtectedDocument.h"
#include "../PPOIS 2/VeryImportantDocument.h"	
#include <iostream>

using namespace Microsoft::VisualStudio::CppUnitTestFramework;
using namespace std;

namespace UnitTest1
{
	TEST_CLASS(DocumentTEST)
	{
	public:
		
		TEST_METHOD(test1)
		{
			// ������������ ������ SetName � GetName
			Document doc;
			string testName = "My Document";
			doc.SetName(testName);
			Assert::AreEqual(doc.GetName(), testName);

			// ������������ ������ SetContent � GetContent
			string testContent = "This is the content of my document.";
			doc.SetContent(testContent);
			Assert::AreEqual(doc.GetContent(), testContent);

			cout << "��� ����� �������� �������!" << endl;
		}
		TEST_METHOD(test2) {
			using namespace AbilityToCopy;
			Document doc;
			string testName = "My Document";
			string testContent = "12345";
			doc.SetContent(testContent);
			doc.SetName(testName);
			Document docCopy = CopyDocument(doc);
			Assert::AreEqual(docCopy.GetName(),doc.GetName() + "_copy");
			Assert::AreEqual(docCopy.GetContent(), doc.GetContent());

			cout << "��� ����� �������� �������!" << endl;
		}
		TEST_METHOD(test3) {
			Document doc;
			APersonWhoCanWrite bob;
			string testName = "My Document";
			string testContent = "12345";
			string AssumedOutput = "\nName of the document: My Document\n12345";
			doc.SetContent(testContent);
			doc.SetName(testName);
			string RealOutput = bob.PrintAllContent(doc);
			Assert::AreEqual(RealOutput, AssumedOutput);
			cout << "��� ����� �������� �������!" << endl;
		}
		TEST_METHOD(test4) {
			// ������������ ������ SetName � GetName
			PrivateDocument doc;
			string testName = "My Document";
			doc.SetPrivateName(testName);
			Assert::AreEqual(doc.GetPrivateName(), testName);

			// ������������ ������ SetContent � GetContent
			string testContent = "This is the content of my document.";
			doc.SetPrivateContent(testContent);
			Assert::AreEqual(doc.GetPrivateContent(), testContent);

			cout << "��� ����� �������� �������!" << endl;
		}
		TEST_METHOD(test5) {
			// ������������ ������ SetName � GetName
			ProtectedDocument doc;
			string testName = "My Document";
			doc.SetProtectedName(testName);
			Assert::AreEqual(doc.GetProtectedName(), testName);

			// ������������ ������ SetContent � GetContent
			string testContent = "This is the content of my document.";
			doc.SetProtectedContent(testContent);
			Assert::AreEqual(doc.GetProtectedContent(), testContent);

			cout << "��� ����� �������� �������!" << endl;
		}
	};
}
