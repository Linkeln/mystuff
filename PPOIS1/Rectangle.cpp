#include "Rectangle.h"
using namespace std;
#include <iostream>
Rectangle::Rectangle(int ax, int bx, int ay, int by) {
    this->ax = ax;
    this->ay = ay;
    this->bx = bx;
    this->by = by;
}
int MaxOutOfFour(int a, int b, int c, int d) {
    int max;
    max = a;
    if (b > max)
        max = b;
    if (c > max)
        max = c;
    if (d > max)
        max = d;
    return max;
}

int MinOutOfFour(int a, int b, int c, int d) {
    int min;
    min = a;
    if (b < min)
        min = b;
    if (c < min)
        min = c;
    if (d < min)
        min = d;
    return min;
}
void Rectangle::move(int dx, int dy) {
        this->ax += dx;
        this->ay += dy;
        this->bx += dx;
        this->by += dy;

}
    int* Rectangle::GetCoordinates() {
        cout << "Первая точка:\nX = " << ax << "\nY = " << ay;
        cout << "Вторая точка:\nX = " << bx << "\nY = " << by;
        int* coords = new int[4];
        coords[0] = this->ax;
        coords[1] = this->bx;
        coords[2] = this->ay;
        coords[3] = this->by;
        return coords;

    }
    void Rectangle::ChangeScale(int dx, int dy) {
        if (this->ax > this->bx) {
            this->ax += dx;
            this->bx -= dx;
        }
        else {
            this->ax -= dx;
            this->bx += dx;
        }
        if (this->ay > this->by) {
            this->ay += dy;
            this->by -= dy;
        }
        else {
            this->ay -= dy;
            this->by += dy;
        }
    }
Rectangle& Rectangle :: operator--() {
    //все эти бесконечные if для того, чтобы определить какая из точек по какой оси дальше от начала координат, чтобы прямоугольник всегда раздувался
        if (this->ax > this->bx) {
            this->ax--;
            this->bx++;
        }
        else {
            this->ax++;
            this->bx--;
        }
        if (this->ay > this->by) {
            this->ay--;
            this->by++;
        }
        else {
            this->ay++;
            this->by--;
        }
        return *this;
    }
Rectangle& Rectangle :: operator++() {
    //все эти бесконечные if для того, чтобы определить какая из точек по какой оси дальше от начала координат, чтобы прямоугольник всегда раздувался
    if (this->ax > this->bx) {
        this->ax++;
        this->bx--;
    }
    else {
        this->ax--;
        this->bx++;
    }
    if (this->ay > this->by) {
        this->ay++;
        this->by--;
    }
    else {
        this->ay--;
        this->by++;
    }
    return *this;
}
Rectangle& Rectangle::operator + (const Rectangle& SecondRectangle) { //простите меня за функцию, что будет дальше
    Rectangle FunctionResult(
        MinOutOfFour(this->ax, this->bx, SecondRectangle.ax, SecondRectangle.bx),
        MinOutOfFour(this->ay, this->by, SecondRectangle.ay, SecondRectangle.by),
        MaxOutOfFour(this->ax, this->bx, SecondRectangle.ax, SecondRectangle.bx), 
        MinOutOfFour(this->ay, this->by, SecondRectangle.ay, SecondRectangle.by));
    return FunctionResult;
}
Rectangle& Rectangle::operator += (const Rectangle& SecondRectangle) { //простите меня за функцию, что будет дальше
    this->ax = MinOutOfFour(this->ax, this->bx, SecondRectangle.ax, SecondRectangle.bx);
    this->ay = MinOutOfFour(this->ay, this->by, SecondRectangle.ay, SecondRectangle.by);
    this->bx = MaxOutOfFour(this->ax, this->bx, SecondRectangle.ax, SecondRectangle.bx);
    this->by = MaxOutOfFour(this->ay, this->by, SecondRectangle.ay, SecondRectangle.by);
    return *this;
}
Rectangle& Rectangle::operator - (const Rectangle& SecondRectangle) {

    int LeftSideFirst, RightSideFirst, UpperSideFirst, LowerSideFirst;
    int LeftSideSecond, RightSideSecond, UpperSideSecond, LowerSideSecond;
    int LeftSideThird, RightSideThird, UpperSideThird, LowerSideThird;
    if (this->ax > this->bx) {
        RightSideFirst = this->ax;              //я из принципа не хотел смотреть в интернете как делать пересечение прямоугольников
        LeftSideFirst = this->bx;               //так что решение ни разу не оптимальное, зато своё
    }
    else{
        RightSideFirst = this->bx;              //здесь мы определяем стороны прямоугольников и заносим их в соответствующие переменные
        LeftSideFirst = this->ax;               //итого у нас получается 8 сторон по 4 на каждый прямоугольник, причем мы знаем, какая из них правая, а какая левая и т.п.
    }
    if (this->ay > this->by) {
        UpperSideFirst = this->ay;
        LowerSideFirst = this->by;
    }
    else {
        UpperSideFirst = this->by;
        LowerSideFirst = this->ay;
    }

    if (SecondRectangle.ax > SecondRectangle.bx) {
        RightSideSecond = SecondRectangle.ax;
        LeftSideSecond = SecondRectangle.bx;
    }
    else {
        RightSideSecond = SecondRectangle.bx;
        LeftSideSecond = SecondRectangle.ax;
    }
    if (SecondRectangle.ay > SecondRectangle.by) {
        UpperSideSecond = SecondRectangle.ay;
        LowerSideSecond = SecondRectangle.by;
    }
    else {
        UpperSideSecond = SecondRectangle.by;
        LowerSideSecond = SecondRectangle.ay;
    }
    if (RightSideFirst < LeftSideSecond || LeftSideFirst > RightSideSecond || LowerSideFirst > UpperSideSecond || LowerSideSecond > UpperSideFirst) {
        Rectangle NoIntersections(0, 0, 0, 0); //здесь мы проверяем нет ли такого, что у одного прямоугольника левая сторона правее правой второго и т.п
        return NoIntersections; //в случае, если такое произошло выводим прямоугольник 0 0 0 0, потому что пересечений нет
    }
        
    
    if (LeftSideFirst > LeftSideSecond)
        LeftSideThird = LeftSideFirst;
    else
        LeftSideThird = LeftSideSecond;
    if (RightSideFirst > RightSideSecond)
        RightSideThird = RightSideSecond;
    else
        RightSideThird = RightSideFirst;
    if (UpperSideFirst > UpperSideSecond)
        UpperSideThird = UpperSideSecond;
    else
        UpperSideThird = UpperSideFirst;
    if (LowerSideFirst > LowerSideFirst)
        LowerSideThird = LowerSideFirst;
    else
        LowerSideThird = LowerSideSecond;
    Rectangle FunctionResult(LeftSideThird, LowerSideThird, RightSideThird, UpperSideThird);
    return FunctionResult;
}

Rectangle& Rectangle::operator -= (const Rectangle& SecondRectangle) {

    int LeftSideFirst, RightSideFirst, UpperSideFirst, LowerSideFirst;
    int LeftSideSecond, RightSideSecond, UpperSideSecond, LowerSideSecond;
    int LeftSideThird, RightSideThird, UpperSideThird, LowerSideThird;
    if (this->ax > this->bx) {
        RightSideFirst = this->ax;              //я из принципа не хотел смотреть в интернете как делать пересечение прямоугольников
        LeftSideFirst = this->bx;               //так что решение ни разу не оптимальное, зато своё
    }
    else {
        RightSideFirst = this->bx;              //здесь мы определяем стороны прямоугольников и заносим их в соответствующие переменные
        LeftSideFirst = this->ax;               //итого у нас получается 8 сторон по 4 на каждый прямоугольник, причем мы знаем, какая из них правая, а какая левая и т.п.
    }
    if (this->ay > this->by) {
        UpperSideFirst = this->ay;
        LowerSideFirst = this->by;
    }
    else {
        UpperSideFirst = this->by;
        LowerSideFirst = this->ay;
    }

    if (SecondRectangle.ax > SecondRectangle.bx) {
        RightSideSecond = SecondRectangle.ax;
        LeftSideSecond = SecondRectangle.bx;
    }
    else {
        RightSideSecond = SecondRectangle.bx;
        LeftSideSecond = SecondRectangle.ax;
    }
    if (SecondRectangle.ay > SecondRectangle.by) {
        UpperSideSecond = SecondRectangle.ay;
        LowerSideSecond = SecondRectangle.by;
    }
    else {
        UpperSideSecond = SecondRectangle.by;
        LowerSideSecond = SecondRectangle.ay;
    }
    if (RightSideFirst < LeftSideSecond || LeftSideFirst > RightSideSecond || LowerSideFirst > UpperSideSecond || LowerSideSecond > UpperSideFirst) {
        Rectangle NoIntersections(0, 0, 0, 0); //здесь мы проверяем нет ли такого, что у одного прямоугольника левая сторона правее правой второго и т.п
        return NoIntersections; //в случае, если такое произошло выводим прямоугольник 0 0 0 0, потому что пересечений нет
    }

 
    if (LeftSideFirst > LeftSideSecond)
        LeftSideThird = LeftSideFirst;
    else
        LeftSideThird = LeftSideSecond;
    if (RightSideFirst > RightSideSecond)
        RightSideThird = RightSideSecond;
    else
        RightSideThird = RightSideFirst;
    if (UpperSideFirst > UpperSideSecond)
        UpperSideThird = UpperSideSecond;
    else
        UpperSideThird = UpperSideFirst;
    if (LowerSideFirst > LowerSideFirst)
        LowerSideThird = LowerSideFirst;
    else
        LowerSideThird = LowerSideSecond;

    this->ax = LeftSideThird;
    this->ay = LowerSideThird;
    this->bx = RightSideThird;
    this->by = UpperSideThird;
    return *this;
}



    