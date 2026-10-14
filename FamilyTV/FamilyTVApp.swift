import SwiftUI

// Customize titles, colors and cards here; sample data lives in Core/FamilyState.swift.
@main struct TVStarterApp: App {
    var body: some Scene { WindowGroup { Dashboard() } }
}
struct Dashboard: View {
    @AppStorage("starter-dark") private var dark = true
    @State private var state = FamilyState.sample()
    @State private var page = "Today"
    @State private var selected: String?
    private let accent = Color(red: 0.40, green: 0.85, blue: 0.79)
    var body: some View {
        ZStack {
            (dark ? Color(red: 0.06, green: 0.10, blue: 0.15) : Color(red: 0.96, green: 0.94, blue: 0.89)).ignoresSafeArea()
            VStack(alignment: .leading, spacing: 35) {
                HStack {
                    Text("TV / STARTER").font(.system(size: 22, weight: .bold)).tracking(4)
                    Spacer()
                    ForEach(["Today", "Practice", "Settings"], id: \.self) { name in
                        Button(name) { page = name }.tint(accent)
                    }
                }
                if page == "Today" {
                    Text("A little space for your everyday.").font(.system(size: 56, weight: .medium, design: .serif))
                    Text("An offline sample. Make it your own.").font(.system(size: 24)).foregroundStyle(accent)
                    HStack(spacing: 25) {
                        tile("Explore", "Mountains", "mountain.2.fill", .blue)
                        tile("Create", "Your next idea", "sparkles", .purple)
                        tile("Unwind", "A quiet moment", "leaf.fill", .teal)
                    }.frame(height: 220)
                    HStack(alignment: .top, spacing: 55) {
                        VStack(alignment: .leading, spacing: 18) {
                            Text("ON THE MENU").foregroundStyle(accent)
                            Text(state.dinner).font(.system(size: 32, design: .serif))
                        }
                        VStack(alignment: .leading, spacing: 18) {
                            Text("LITTLE REMINDERS").foregroundStyle(accent)
                            ForEach(state.reminders, id: \.self) { Text($0).font(.system(size: 25)) }
                        }
                        Spacer()
                    }.padding(30)
                } else if page == "Practice" {
                    Text("Small steps, every day.").font(.system(size: 48, design: .serif))
                    ForEach(state.tasks.indices, id: \.self) { i in
                        Button {
                            state.tasks[i].toggle(on: Date())
                        } label: {
                            HStack {
                                Image(systemName: state.tasks[i].symbol)
                                Text("\(state.tasks[i].child) · \(state.tasks[i].title)")
                                Spacer()
                                Text(state.tasks[i].isDone(on: Date()) ? "Done ✓" : "\(state.tasks[i].minutes) minutes")
                            }.padding(15)
                        }
                    }
                    Text("Practice check-offs are in memory in this sample.").font(.system(size: 22))
                } else {
                    Text("Your TV, your style.").font(.system(size: 48, design: .serif))
                    Toggle("Dark appearance", isOn: $dark)
                    Button("Reset sample data") { state = FamilyState.sample() }
                    Text("No account, network connection, or personal data required.").font(.system(size: 24))
                }
                Spacer()
                Text("Use your remote to explore · Select to open · Back to return").font(.system(size: 20)).foregroundStyle(accent)
            }.padding(70)
        }.foregroundStyle(dark ? .white : .black)
        .preferredColorScheme(dark ? .dark : .light)
        .onExitCommand { page = "Today" }
        .fullScreenCover(item: Binding(get: { selected.map { Selection(title: $0) } }, set: { selected = $0?.title })) { item in
            VStack(spacing: 40) {
                Image(systemName: "sparkles").font(.system(size: 110)).foregroundStyle(accent)
                Text(item.title).font(.system(size: 60, design: .serif))
                Text("Replace this screen with your custom experience.").font(.system(size: 28))
                Button("Back to dashboard") { selected = nil }
            }.onExitCommand { selected = nil }
        }
    }
    private func tile(_ title: String, _ detail: String, _ symbol: String, _ color: Color) -> some View {
        Button { selected = title } label: {
            VStack(alignment: .leading, spacing: 15) {
                Image(systemName: symbol).font(.system(size: 55))
                Text(title).font(.system(size: 32, weight: .medium, design: .serif))
                Text(detail).font(.system(size: 22))
            }.frame(maxWidth: .infinity, alignment: .leading).padding(28).background(color.opacity(0.20), in: RoundedRectangle(cornerRadius: 24))
        }.buttonStyle(.card)
    }
}
private struct Selection: Identifiable { let title: String; var id: String { title } }
