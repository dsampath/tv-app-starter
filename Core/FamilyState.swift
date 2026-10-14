import Foundation

struct Countdown: Codable, Identifiable, Equatable {
    var id = UUID()
    var title: String
    var date: Date
    func daysRemaining(now: Date, calendar: Calendar = .current) -> Int {
        calendar.dateComponents([.day], from: calendar.startOfDay(for: now), to: calendar.startOfDay(for: date)).day ?? 0
    }
}

struct PracticeTask: Codable, Identifiable, Equatable {
    var id: String
    var child: String
    var title: String
    var minutes: Int
    var symbol: String
    var completedDays: Set<String> = []
    func isDone(on date: Date, calendar: Calendar = .current) -> Bool {
        completedDays.contains(Self.dayKey(date, calendar: calendar))
    }
    mutating func toggle(on date: Date, calendar: Calendar = .current) {
        let key = Self.dayKey(date, calendar: calendar)
        if completedDays.contains(key) { completedDays.remove(key) } else { completedDays.insert(key) }
    }
    func streak(on date: Date, calendar: Calendar = .current) -> Int {
        var day = calendar.startOfDay(for: date)
        if !isDone(on: day, calendar: calendar) { day = calendar.date(byAdding: .day, value: -1, to: day)! }
        var count = 0
        while isDone(on: day, calendar: calendar) {
            count += 1
            guard let previous = calendar.date(byAdding: .day, value: -1, to: day) else { break }
            day = previous
        }
        return count
    }
    static func dayKey(_ date: Date, calendar: Calendar) -> String {
        let c = calendar.dateComponents([.year, .month, .day], from: date)
        return String(format: "%04d-%02d-%02d", c.year!, c.month!, c.day!)
    }
}

struct FamilyState: Codable, Equatable {
    var familyName = "Our family"
    var dinner = "Veggie tacos"
    var reminders = ["Pack lunches + water bottles", "Return library books"]
    var countdowns: [Countdown] = []
    var tasks = [PracticeTask(id: "guitar", child: "Alex", title: "Guitar practice", minutes: 20, symbol: "guitars"),
                 PracticeTask(id: "piano", child: "Child 2", title: "Piano practice", minutes: 15, symbol: "pianokeys")]
    var calendars = ["Family": true, "School": true, "Activities": true]
    var rotatePhotos = true
    var photoSeconds = 60
    var keepAwake = true
    var showPhotos = true
    var showMeals = true
    var showCountdowns = true
    var celebratePractice = true
    static func sample(now: Date = Date()) -> FamilyState {
        var state = FamilyState()
        state.countdowns = [Countdown(title: "Family getaway", date: Calendar.current.date(byAdding: .day, value: 42, to: now)!)]
        return state
    }
}

enum LocalRequest {
    static func apply(_ request: String, to state: inout FamilyState, now: Date = Date()) -> String {
        let trimmed = request.trimmingCharacters(in: .whitespacesAndNewlines)
        let lower = trimmed.lowercased()
        if lower == "lunches are packed" {
            state.reminders.removeAll { $0 == "Pack lunches + water bottles" }
            return "Lunch packing is checked off."
        }
        if lower.hasPrefix("dinner: ") {
            let meal = String(trimmed.dropFirst(8)).trimmingCharacters(in: .whitespaces)
            guard !meal.isEmpty else { return "Add a meal after Dinner:." }
            state.dinner = meal
            return "Tonight’s dinner is now \(meal)."
        }
        if lower.hasPrefix("remind me: ") {
            let reminder = String(trimmed.dropFirst(11)).trimmingCharacters(in: .whitespaces)
            guard !reminder.isEmpty else { return "Add a reminder after Remind me:." }
            if !state.reminders.contains(reminder) { state.reminders.append(reminder) }
            return "Added your reminder to the dashboard."
        }
        if lower.hasPrefix("countdown: "), let range = trimmed.range(of: " on ", options: [.backwards, .caseInsensitive]) {
            let title = String(trimmed[trimmed.index(trimmed.startIndex, offsetBy: 11)..<range.lowerBound]).trimmingCharacters(in: .whitespaces)
            let input = String(trimmed[range.upperBound...]).trimmingCharacters(in: .whitespaces)
            let formatter = DateFormatter()
            formatter.locale = Locale(identifier: "en_US_POSIX")
            formatter.calendar = Calendar(identifier: .gregorian)
            formatter.dateFormat = "yyyy-MM-dd"
            formatter.isLenient = false
            guard !title.isEmpty, let date = formatter.date(from: input), formatter.string(from: date) == input else {
                return "Use Countdown: Vacation on YYYY-MM-DD with a valid date."
            }
            guard Calendar.current.startOfDay(for: date) >= Calendar.current.startOfDay(for: now) else { return "Choose today or a future date." }
            state.countdowns.append(Countdown(title: title, date: date))
            return "Added \(title) to your countdowns."
        }
        return "This local demo supports Dinner: …, Remind me: …, Countdown: … on YYYY-MM-DD, and Lunches are packed. Live AI isn’t connected yet."
    }
}
