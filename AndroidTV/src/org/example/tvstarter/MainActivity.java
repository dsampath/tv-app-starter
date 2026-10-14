package org.example.tvstarter;

import android.app.Activity;
import android.os.Bundle;
import android.graphics.Color;
import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.view.View;
import android.widget.*;

/** Offline, remote-first sample: customize cards and sample text here. */
public class MainActivity extends Activity {
    private LinearLayout content;
    private Button activeTab;
    private String page = "Today";
    private boolean dark;
    private boolean[] done = {false, false};
    private int ink, background;
    private final int accent = Color.rgb(101,217,202);
    @Override public void onCreate(Bundle saved) {
        super.onCreate(saved);
        dark = getPreferences(0).getBoolean("dark", true);
        if (saved != null) { page = saved.getString("page", "Today"); done = saved.getBooleanArray("done"); }
        render();
    }
    @Override public void onSaveInstanceState(Bundle out) { super.onSaveInstanceState(out); out.putString("page", page); out.putBooleanArray("done", done); }
    private int dp(int n) { return (int)(n * getResources().getDisplayMetrics().density); }
    private TextView text(String value, int size) {
        TextView t = new TextView(this); t.setText(value); t.setTextSize(size); t.setTextColor(ink); t.setPadding(0, dp(5),0,dp(5)); return t;
    }
    private Button button(String title, Runnable action) {
        Button b = new Button(this); b.setText(title); b.setTextColor(ink); b.setAllCaps(false); b.setTextSize(18); b.setPadding(dp(16),dp(10),dp(16),dp(10));
        b.setOnClickListener(v -> action.run());
        b.setOnFocusChangeListener((v, focus) -> { GradientDrawable d = new GradientDrawable(); d.setColor(dark ? Color.rgb(32,49,65) : Color.rgb(225,233,229)); d.setCornerRadius(dp(12)); d.setStroke(dp(focus ? 3 : 0),accent); b.setBackground(d); });
        GradientDrawable d = new GradientDrawable(); d.setColor(dark ? Color.rgb(32,49,65) : Color.rgb(225,233,229)); d.setCornerRadius(dp(12)); b.setBackground(d); return b;
    }
    private void render() {
        activeTab = null;
        ink = dark ? Color.WHITE : Color.rgb(20,30,40); background = dark ? Color.rgb(16,26,38) : Color.rgb(245,240,227);
        LinearLayout root = new LinearLayout(this); root.setOrientation(1); root.setPadding(dp(42),dp(24),dp(42),dp(22)); root.setBackgroundColor(background); setContentView(root);
        LinearLayout nav = new LinearLayout(this); TextView brand = text("TV / STARTER",20); brand.setLetterSpacing(.18f); nav.addView(brand,new LinearLayout.LayoutParams(0,-2,1));
        for(String name: new String[]{"Today","Practice","Settings"}) { Button b=button(name,()->{page=name;render();}); if(name.equals(page)) activeTab=b; LinearLayout.LayoutParams p=new LinearLayout.LayoutParams(-2,-2);p.setMargins(dp(8),0,0,0);nav.addView(b,p); }
        root.addView(nav); ScrollView scroll=new ScrollView(this);content=new LinearLayout(this);content.setOrientation(1);content.setPadding(0,dp(20),0,0);scroll.addView(content);root.addView(scroll,new LinearLayout.LayoutParams(-1,0,1));
        if(page.equals("Today")) {
            TextView heading=text("A little space for your everyday.",34);heading.setTypeface(Typeface.SERIF);content.addView(heading);
            TextView sub=text("An offline sample. Make it your own.",17);sub.setTextColor(accent);content.addView(sub);
            LinearLayout cards=new LinearLayout(this);
            String[] titles={"Explore","Create","Unwind"}, details={"Mountains","Your next idea","A quiet moment"};
            for(int i=0;i<3;i++){final String title=titles[i];Button b=button(title+"\n\n"+details[i],()->{page=title;render();});LinearLayout.LayoutParams p=new LinearLayout.LayoutParams(0,dp(125),1);p.setMargins(dp(5),dp(12),dp(5),dp(12));cards.addView(b,p);}
            content.addView(cards);content.addView(text("ON THE MENU",14));content.addView(text("Veggie tacos",25));content.addView(text("LITTLE REMINDERS",14));content.addView(text("Pack lunches + water bottles · Return library books",18));
        } else if(page.equals("Practice")) {
            content.addView(text("Small steps, every day.",32));String[] names={"Alex · Guitar practice · 20 minutes","Child 2 · Piano practice · 15 minutes"};
            for(int i=0;i<2;i++){final int index=i;Button b=button(names[i]+(done[i]?" · Done ✓":""),()->{done[index]=!done[index];render();});content.addView(b);}
            content.addView(text("Practice check-offs are in memory in this sample.",18));
        } else if(page.equals("Settings")) {
            content.addView(text("Your TV, your style.",32));content.addView(button("Toggle dark appearance",()->{dark=!dark;getPreferences(0).edit().putBoolean("dark",dark).apply();render();}));content.addView(button("Reset sample data",()->{done=new boolean[]{false,false};render();}));content.addView(text("No account, network connection, or personal data required.",18));
        } else {
            content.addView(text(page,38));content.addView(text("Replace this screen with your custom experience.",22));content.addView(button("Back to dashboard",()->{page="Today";render();}));
        }
        TextView footer=text("Use your remote to explore · Select to open · Back to return",14);footer.setTextColor(accent);root.addView(footer);
        if(activeTab!=null) activeTab.requestFocus();
    }
    @Override public void onBackPressed(){if(!page.equals("Today")){page="Today";render();}else super.onBackPressed();}
}
