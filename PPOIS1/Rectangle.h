#pragma once
class Rectangle
{ 
public:
        int ax, bx, ay, by;
        Rectangle(int ax, int bx, int ay, int by);
        void move(int dx, int dy);
        int* GetCoordinates();
        void ChangeScale(int dx, int dy);
        Rectangle& operator++();
        Rectangle& operator--();
        Rectangle& operator + (const Rectangle& SecondRectangle);
        Rectangle& operator += (const Rectangle& SecondRectangle);
        Rectangle& operator - (const Rectangle& SecondRectangle);
        Rectangle& operator -= (const Rectangle& SecondRectangle);
};

