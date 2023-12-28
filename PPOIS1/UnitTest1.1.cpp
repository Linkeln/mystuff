#include "pch.h"
#include "CppUnitTest.h"
#include "../PPOIS LABA1/Rectangle.h"

using namespace Microsoft::VisualStudio::CppUnitTestFramework;

namespace UnitTest11
{
	TEST_CLASS(UnitTest11)
	{
	public:
		
		TEST_METHOD(Test1)
		{
			Rectangle RECT(1, 4, 0, 5);
			++RECT;
			Assert::AreEqual(RECT.GetCoordinates()[0], 0);
			Assert::AreEqual(RECT.GetCoordinates()[1], 5);
			Assert::AreEqual(RECT.GetCoordinates()[2], -1);
			Assert::AreEqual(RECT.GetCoordinates()[3], 6);
		}
		TEST_METHOD(Test2)
		{
			Rectangle RECT(1, 4, 0, 5);
			--RECT;
			Assert::AreEqual(RECT.GetCoordinates()[0], 2);
			Assert::AreEqual(RECT.GetCoordinates()[1], 3);
			Assert::AreEqual(RECT.GetCoordinates()[2], 1);
			Assert::AreEqual(RECT.GetCoordinates()[3], 4);
		}
		TEST_METHOD(Test3)
		{
			Rectangle RECT1(1, 4, 0, 5);
			Rectangle RECT2(-2, 5, 1, 8);
			Rectangle Resulat = RECT1 + RECT2;
			Assert::AreEqual(Resulat.GetCoordinates()[0], -2);
			Assert::AreEqual(Resulat.GetCoordinates()[1], 0);
			Assert::AreEqual(Resulat.GetCoordinates()[2], 5);
			Assert::AreEqual(Resulat.GetCoordinates()[3], 0);
		}
		TEST_METHOD(Test4)
		{
			Rectangle RECT1(1, 4, 0, 5);
			Rectangle RECT2(-2, 5, 1, 8);
			Rectangle Resulat = RECT1 - RECT2;
			Assert::AreEqual(Resulat.GetCoordinates()[0], 1);
			Assert::AreEqual(Resulat.GetCoordinates()[1], 1);
			Assert::AreEqual(Resulat.GetCoordinates()[2], 4);
			Assert::AreEqual(Resulat.GetCoordinates()[3], 5);
		}
		TEST_METHOD(Test5)
		{
			Rectangle RECT1(1, 4, 0, 5);
			Rectangle RECT2(-2, 5, 1, 8);
			RECT1 += RECT2;
			Assert::AreEqual(RECT1.GetCoordinates()[0], -2);
			Assert::AreEqual(RECT1.GetCoordinates()[1], 5);
			Assert::AreEqual(RECT1.GetCoordinates()[2], 0);
			Assert::AreEqual(RECT1.GetCoordinates()[3], 8);
		}
		TEST_METHOD(Test6)
		{
			Rectangle RECT1(1, 4, 0, 5);
			Rectangle RECT2(-2, 5, 1, 8);
			RECT1 -= RECT2;
			Assert::AreEqual(RECT1.GetCoordinates()[0], 1);
			Assert::AreEqual(RECT1.GetCoordinates()[1], 4);
			Assert::AreEqual(RECT1.GetCoordinates()[2], 1);
			Assert::AreEqual(RECT1.GetCoordinates()[3], 5);
		}
		TEST_METHOD(Test7) {
			Rectangle RECT(1, 4, 0, 5);
			RECT.move(3, 4);
			Assert::AreEqual(RECT.GetCoordinates()[0], 4);
			Assert::AreEqual(RECT.GetCoordinates()[1], 7);
			Assert::AreEqual(RECT.GetCoordinates()[2], 4);
			Assert::AreEqual(RECT.GetCoordinates()[3], 9);
		}
		TEST_METHOD(Test8) {
			Rectangle RECT(1, 4, 0, 5);
			RECT.ChangeScale(3, 4);
			Assert::AreEqual(RECT.GetCoordinates()[0], -2);
			Assert::AreEqual(RECT.GetCoordinates()[1], 7);
			Assert::AreEqual(RECT.GetCoordinates()[2], -4);
			Assert::AreEqual(RECT.GetCoordinates()[3], 9);
		}
		TEST_METHOD(Test9)
		{
			Rectangle RECT1(5, 0, 8, 1);
			Rectangle RECT2(8, 1, 5, -2);
			RECT1 -= RECT2;
			Assert::AreEqual(RECT1.GetCoordinates()[0], 1);
			Assert::AreEqual(RECT1.GetCoordinates()[1], 5);
			Assert::AreEqual(RECT1.GetCoordinates()[2], -2);
			Assert::AreEqual(RECT1.GetCoordinates()[3], 5);
		}
	};
}
