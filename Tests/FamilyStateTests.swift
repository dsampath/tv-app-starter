import XCTest
@testable import FamilyTVCore

final class FamilyStateTests: XCTestCase {
    var calendar: Calendar { var c = Calendar(identifier: .gregorian); c.timeZone = TimeZone(identifier: "America/Los_Angeles")!; return c }
    func date(_ day: Int, hour: Int = 12) -> Date { calendar.date(from: DateComponents(year: 2026, month: 3, day: day, hour: hour))! }
    func testPracticeResetsAtMidnightAndKeepsHistory() {
        var task = PracticeTask(id: "guitar", child: "Alex", title: "Guitar", minutes: 20, symbol: "guitars")
        task.toggle(on: date(7, hour: 23), calendar: calendar)
        XCTAssertTrue(task.isDone(on: date(7), calendar: calendar))
        XCTAssertFalse(task.isDone(on: date(8), calendar: calendar))
        task.toggle(on: date(8), calendar: calendar)
        XCTAssertEqual(task.streak(on: date(8), calendar: calendar), 2)
        task.toggle(on: date(8), calendar: calendar)
        XCTAssertEqual(task.streak(on: date(8), calendar: calendar), 1)
        XCTAssertEqual(task.streak(on: date(10), calendar: calendar), 0)
    }
    func testCountdownAcrossDaylightSavingUsesCalendarDays() {
        let countdown = Countdown(title: "Trip", date: date(9, hour: 0))
        XCTAssertEqual(countdown.daysRemaining(now: date(7, hour: 23), calendar: calendar), 2)
        XCTAssertEqual(countdown.daysRemaining(now: date(9, hour: 23), calendar: calendar), 0)
    }
    func testInvalidRequestDoesNotMutateState() {
        var state = FamilyState.sample(); let original = state
        _ = LocalRequest.apply("Countdown: Trip on 2027-02-30", to: &state)
        XCTAssertEqual(state, original)
        _ = LocalRequest.apply("Move school pickup", to: &state)
        XCTAssertEqual(state, original)
    }
    func testRequestsAndStorageRoundTrip() throws {
        var state = FamilyState.sample()
        _ = LocalRequest.apply("Dinner: black bean tacos", to: &state)
        _ = LocalRequest.apply("Remind me: Swim bag", to: &state)
        _ = LocalRequest.apply("Remind me: Swim bag", to: &state)
        _ = LocalRequest.apply("Countdown: Trip on 2099-12-20", to: &state)
        XCTAssertEqual(state.dinner, "black bean tacos")
        XCTAssertEqual(state.reminders.filter { $0 == "Swim bag" }.count, 1)
        XCTAssertEqual(state.countdowns.last?.title, "Trip")
        let decoded = try JSONDecoder().decode(FamilyState.self, from: JSONEncoder().encode(state))
        XCTAssertEqual(decoded, state)
    }
}
