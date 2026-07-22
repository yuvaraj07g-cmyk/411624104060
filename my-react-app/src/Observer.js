/*let observers = [];

function attach(observer) {
    observers.push(observer);
}

function detach(name){
    let newObservers=[];
    for(let i of observers){
        if(i!==name){
            newObservers.push(i);
        }
    }
    observers=newObservers;
}

function notify() {
    for (let i of observers) {
        console.log(i + ": Noticed");
    }
}

attach("A");
attach("B");
notify();

attach("C");
detach("B");
notify();*/

/*let students=[];
function attach(student){
    students.push(student);
}
function detach(student){
    let newStudents=[];
    for(let i of students){
        if(i!==student){
            newStudents.push(i);
        }
    }
    students=newStudents;
}
function notify(announcement){
    for(let i of students){
        console.log(i+" received announcement: "+announcement);
    }
}
attach("Rahul");
attach("Priya");
attach("Kavin");
console.log("Holiday Announcement");
notify("Tomorrow is a Holiday");
console.log();
console.log("Exam Announcement");
notify("Mid-Term Exams start from Monday");
console.log();
console.log("Fest Announcement");
notify("Annual Cultural Fest is on Friday");
detach("Priya");
console.log();
console.log("After Priya Unsubscribed");
notify("Sports Day will be held next week");*/

const age=18;

if(age<18){
    console.log("Not Eligible");
}else if(age==18){
    console.log();
}else{
    console.log("Eligible");
}