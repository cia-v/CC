"""
车工计算软件 - Android 版本
基于 Kivy 框架的移动端应用
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.core.window import Window
from kivy.metrics import dp

# 导入计算模块
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lathe_calculator.basic_calc import (
    calculate_cutting_speed,
    calculate_spindle_speed,
    calculate_feed_rate,
    calculate_cutting_depth
)
from lathe_calculator.thread_calc import (
    calculate_metric_thread,
    calculate_imperial_thread,
    generate_g92_cycle,
    generate_g76_cycle
)
from lathe_calculator.taper_arc_calc import (
    calculate_taper,
    calculate_arc_interpolation
)
from lathe_calculator.data_manager import MaterialLibrary, ToolLibrary


class LatheCalculatorApp(App):
    def build(self):
        Window.clearcolor = (0.95, 0.95, 0.95, 1)
        
        # 创建主布局
        main_layout = BoxLayout(orientation='vertical')
        
        # 标题
        title_label = Label(
            text='车工计算软件 v1.0',
            size_hint_y=None,
            height=dp(50),
            font_size=dp(20),
            bold=True,
            color=(0.2, 0.4, 0.6, 1)
        )
        main_layout.add_widget(title_label)
        
        # 创建标签页面板
        self.tab_panel = TabbedPanel()
        self.tab_panel.default_tab_text = '基础计算'
        self.tab_panel.tab_width = dp(120)
        
        # 添加各个功能标签页
        self.tab_panel.add_widget(self.create_basic_calc_tab())
        self.tab_panel.add_widget(self.create_thread_calc_tab())
        self.tab_panel.add_widget(self.create_taper_arc_tab())
        self.tab_panel.add_widget(self.create_data_lib_tab())
        
        main_layout.add_widget(self.tab_panel)
        
        return main_layout
    
    def create_basic_calc_tab(self):
        """创建基础参数计算标签页"""
        tab = TabbedPanelHeader(text='基础计算')
        scroll = ScrollView()
        layout = GridLayout(cols=1, spacing=dp(10), size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        
        # R01: 切削速度计算
        section1 = self.create_section('切削速度计算 (R01)')
        self.diameter_input = TextInput(hint_text='工件直径 (mm)', multiline=False, size_hint_y=None, height=dp(40))
        self.rpm_input = TextInput(hint_text='主轴转速 (rpm)', multiline=False, size_hint_y=None, height=dp(40))
        calc_vc_btn = Button(text='计算切削速度', size_hint_y=None, height=dp(45))
        calc_vc_btn.bind(on_press=self.on_calculate_vc)
        self.vc_result = Label(text='结果将显示在这里', size_hint_y=None, height=dp(40), color=(0.2, 0.5, 0.2, 1))
        
        section1.add_widget(self.diameter_input)
        section1.add_widget(self.rpm_input)
        section1.add_widget(calc_vc_btn)
        section1.add_widget(self.vc_result)
        layout.add_widget(section1)
        
        # R02: 主轴转速计算
        section2 = self.create_section('主轴转速计算 (R02)')
        self.vc_input = TextInput(hint_text='切削速度 (m/min)', multiline=False, size_hint_y=None, height=dp(40))
        self.dia_for_rpm = TextInput(hint_text='工件直径 (mm)', multiline=False, size_hint_y=None, height=dp(40))
        calc_rpm_btn = Button(text='计算主轴转速', size_hint_y=None, height=dp(45))
        calc_rpm_btn.bind(on_press=self.on_calculate_rpm)
        self.rpm_result = Label(text='结果将显示在这里', size_hint_y=None, height=dp(40), color=(0.2, 0.5, 0.2, 1))
        
        section2.add_widget(self.vc_input)
        section2.add_widget(self.dia_for_rpm)
        section2.add_widget(calc_rpm_btn)
        section2.add_widget(self.rpm_result)
        layout.add_widget(section2)
        
        # R03: 进给量计算
        section3 = self.create_section('进给量计算 (R03)')
        self.feed_per_rev = TextInput(hint_text='每转进给 (mm/r)', multiline=False, size_hint_y=None, height=dp(40))
        self.rpm_for_feed = TextInput(hint_text='主轴转速 (rpm)', multiline=False, size_hint_y=None, height=dp(40))
        calc_feed_btn = Button(text='计算进给速度', size_hint_y=None, height=dp(45))
        calc_feed_btn.bind(on_press=self.on_calculate_feed)
        self.feed_result = Label(text='结果将显示在这里', size_hint_y=None, height=dp(40), color=(0.2, 0.5, 0.2, 1))
        
        section3.add_widget(self.feed_per_rev)
        section3.add_widget(self.rpm_for_feed)
        section3.add_widget(calc_feed_btn)
        section3.add_widget(self.feed_result)
        layout.add_widget(section3)
        
        # R04: 切削深度计算
        section4 = self.create_section('切削深度计算 (R04)')
        self.blank_dia = TextInput(hint_text='毛坯直径 (mm)', multiline=False, size_hint_y=None, height=dp(40))
        self.finish_dia = TextInput(hint_text='成品直径 (mm)', multiline=False, size_hint_y=None, height=dp(40))
        calc_depth_btn = Button(text='计算切削深度', size_hint_y=None, height=dp(45))
        calc_depth_btn.bind(on_press=self.on_calculate_depth)
        self.depth_result = Label(text='结果将显示在这里', size_hint_y=None, height=dp(40), color=(0.2, 0.5, 0.2, 1))
        
        section4.add_widget(self.blank_dia)
        section4.add_widget(self.finish_dia)
        section4.add_widget(calc_depth_btn)
        section4.add_widget(self.depth_result)
        layout.add_widget(section4)
        
        scroll.add_widget(layout)
        tab.content = scroll
        return tab
    
    def create_thread_calc_tab(self):
        """创建螺纹加工计算标签页"""
        tab = TabbedPanelHeader(text='螺纹加工')
        scroll = ScrollView()
        layout = GridLayout(cols=1, spacing=dp(10), size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        
        # R05: 公制螺纹计算
        section1 = self.create_section('公制螺纹参数 (R05)')
        self.thread_major_dia = TextInput(hint_text='大径 (mm)', multiline=False, size_hint_y=None, height=dp(40))
        self.thread_pitch = TextInput(hint_text='螺距 P (mm)', multiline=False, size_hint_y=None, height=dp(40))
        calc_metric_btn = Button(text='计算螺纹参数', size_hint_y=None, height=dp(45))
        calc_metric_btn.bind(on_press=self.on_calculate_metric_thread)
        self.metric_thread_result = Label(text='结果将显示在这里', size_hint_y=None, height=dp(80), color=(0.2, 0.5, 0.2, 1))
        
        section1.add_widget(self.thread_major_dia)
        section1.add_widget(self.thread_pitch)
        section1.add_widget(calc_metric_btn)
        section1.add_widget(self.metric_thread_result)
        layout.add_widget(section1)
        
        # R06: 英制螺纹计算
        section2 = self.create_section('英制螺纹参数 (R06)')
        self.imp_major_dia = TextInput(hint_text='大径 (英寸)', multiline=False, size_hint_y=None, height=dp(40))
        self.tpi_input = TextInput(hint_text='每英寸牙数 TPI', multiline=False, size_hint_y=None, height=dp(40))
        calc_imp_btn = Button(text='计算英制螺纹', size_hint_y=None, height=dp(45))
        calc_imp_btn.bind(on_press=self.on_calculate_imperial_thread)
        self.imp_thread_result = Label(text='结果将显示在这里', size_hint_y=None, height=dp(80), color=(0.2, 0.5, 0.2, 1))
        
        section2.add_widget(self.imp_major_dia)
        section2.add_widget(self.tpi_input)
        section2.add_widget(calc_imp_btn)
        section2.add_widget(self.imp_thread_result)
        layout.add_widget(section2)
        
        scroll.add_widget(layout)
        tab.content = scroll
        return tab
    
    def create_taper_arc_tab(self):
        """创建锥度与圆弧计算标签页"""
        tab = TabbedPanelHeader(text='锥度/圆弧')
        scroll = ScrollView()
        layout = GridLayout(cols=1, spacing=dp(10), size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        
        # R08: 圆锥锥度计算
        section1 = self.create_section('圆锥锥度计算 (R08)')
        self.taper_large_dia = TextInput(hint_text='大端直径 (mm)', multiline=False, size_hint_y=None, height=dp(40))
        self.taper_small_dia = TextInput(hint_text='小端直径 (mm)', multiline=False, size_hint_y=None, height=dp(40))
        self.taper_length = TextInput(hint_text='圆锥长度 (mm)', multiline=False, size_hint_y=None, height=dp(40))
        calc_taper_btn = Button(text='计算锥度参数', size_hint_y=None, height=dp(45))
        calc_taper_btn.bind(on_press=self.on_calculate_taper)
        self.taper_result = Label(text='结果将显示在这里', size_hint_y=None, height=dp(80), color=(0.2, 0.5, 0.2, 1))
        
        section1.add_widget(self.taper_large_dia)
        section1.add_widget(self.taper_small_dia)
        section1.add_widget(self.taper_length)
        section1.add_widget(calc_taper_btn)
        section1.add_widget(self.taper_result)
        layout.add_widget(section1)
        
        scroll.add_widget(layout)
        tab.content = scroll
        return tab
    
    def create_data_lib_tab(self):
        """创建数据管理标签页"""
        tab = TabbedPanelHeader(text='材料/刀具库')
        scroll = ScrollView()
        layout = GridLayout(cols=1, spacing=dp(10), size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        
        # 材料库展示
        section1 = self.create_section('材料库 (R14)')
        mat_lib = MaterialLibrary()
        materials = mat_lib.list_all_materials()
        mat_text = f"材料库共 {len(materials)} 种材料:\n\n"
        for mat in materials[:5]:  # 只显示前5个
            mat_text += f"- {mat['name_cn']} ({mat['name_en']})\n"
        mat_text += "\n... 更多材料可在桌面版查看"
        
        mat_label = Label(text=mat_text, size_hint_y=None, height=dp(150), color=(0.2, 0.4, 0.6, 1))
        section1.add_widget(mat_label)
        layout.add_widget(section1)
        
        # 刀具库展示
        section2 = self.create_section('刀具库 (R15)')
        tool_lib = ToolLibrary()
        tools = tool_lib.list_all_tools()
        tool_text = f"刀具库共 {len(tools)} 种刀具:\n\n"
        for tool in tools[:5]:  # 只显示前5个
            tool_text += f"- {tool['name']}\n  刀尖半径: {tool['nose_radius']}mm\n"
        tool_text += "\n... 更多刀具可在桌面版查看"
        
        tool_label = Label(text=tool_text, size_hint_y=None, height=dp(150), color=(0.2, 0.4, 0.6, 1))
        section2.add_widget(tool_label)
        layout.add_widget(section2)
        
        scroll.add_widget(layout)
        tab.content = scroll
        return tab
    
    def create_section(self, title):
        """创建带标题的区域"""
        container = BoxLayout(orientation='vertical', spacing=dp(5), padding=dp(10))
        title_label = Label(
            text=title,
            size_hint_y=None,
            height=dp(30),
            font_size=dp(16),
            bold=True,
            color=(0.3, 0.5, 0.7, 1)
        )
        container.add_widget(title_label)
        return container
    
    # 事件处理函数
    def on_calculate_vc(self, instance):
        try:
            diameter = float(self.diameter_input.text)
            rpm = float(self.rpm_input.text)
            vc = calculate_cutting_speed(diameter, rpm)
            self.vc_result.text = f"切削速度: {vc:.2f} m/min\n公式: Vc = π × D × n / 1000"
        except ValueError:
            self.vc_result.text = "请输入有效数字"
    
    def on_calculate_rpm(self, instance):
        try:
            vc = float(self.vc_input.text)
            diameter = float(self.dia_for_rpm.text)
            rpm_exact, rpm_rounded, recommended = calculate_spindle_speed(vc, diameter)
            self.rpm_result.text = f"精确转速: {rpm_exact:.0f} rpm\n四舍五入: {rpm_rounded} rpm\n推荐档位: {recommended} rpm"
        except ValueError:
            self.rpm_result.text = "请输入有效数字"
    
    def on_calculate_feed(self, instance):
        try:
            feed_per_rev = float(self.feed_per_rev.text)
            rpm = float(self.rpm_for_feed.text)
            feed_rate = calculate_feed_rate(feed_per_rev=feed_per_rev, spindle_speed=rpm)
            self.feed_result.text = f"进给速度: {feed_rate:.2f} mm/min"
        except ValueError:
            self.feed_result.text = "请输入有效数字"
    
    def on_calculate_depth(self, instance):
        try:
            blank_dia = float(self.blank_dia.text)
            finish_dia = float(self.finish_dia.text)
            depth_single, depth_double, suggestion = calculate_cutting_depth(blank_dia, finish_dia)
            self.depth_result.text = f"单边切深: {depth_single:.2f} mm\n双边切深: {depth_double:.2f} mm\n建议: {suggestion}"
        except ValueError:
            self.depth_result.text = "请输入有效数字"
    
    def on_calculate_metric_thread(self, instance):
        try:
            major_dia = float(self.thread_major_dia.text)
            pitch = float(self.thread_pitch.text)
            result = calculate_metric_thread(major_dia, pitch)
            
            result_text = f"中径: {result['pitch_diameter']:.4f} mm\n"
            result_text += f"小径: {result['minor_diameter']:.4f} mm\n"
            result_text += f"牙高: {result['thread_height']:.4f} mm\n"
            result_text += f"螺旋升角: {result['helix_angle_deg']:.2f}°\n"
            result_text += f"分层切削: {result['passes']} 刀"
            
            self.metric_thread_result.text = result_text
        except ValueError:
            self.metric_thread_result.text = "请输入有效数字"
    
    def on_calculate_imperial_thread(self, instance):
        try:
            major_dia_inch = float(self.imp_major_dia.text)
            tpi = float(self.tpi_input.text)
            result = calculate_imperial_thread(major_dia_inch, tpi)
            
            result_text = f"公制螺距: {result['metric_pitch']:.4f} mm\n"
            result_text += f"中径: {result['pitch_diameter_mm']:.4f} mm\n"
            result_text += f"小径: {result['minor_diameter_mm']:.4f} mm\n"
            result_text += f"牙高: {result['thread_height_mm']:.4f} mm"
            
            self.imp_thread_result.text = result_text
        except ValueError:
            self.imp_thread_result.text = "请输入有效数字"
    
    def on_calculate_taper(self, instance):
        try:
            large_dia = float(self.taper_large_dia.text)
            small_dia = float(self.taper_small_dia.text)
            length = float(self.taper_length.text)
            result = calculate_taper(large_dia, small_dia, length)
            
            result_text = f"锥度比: 1:{result['taper_ratio']:.2f}\n"
            result_text += f"半角: {result['half_angle_deg']:.2f}°\n"
            result_text += f"全角: {result['full_angle_deg']:.2f}°"
            
            self.taper_result.text = result_text
        except ValueError:
            self.taper_result.text = "请输入有效数字"


if __name__ == '__main__':
    LatheCalculatorApp().run()
