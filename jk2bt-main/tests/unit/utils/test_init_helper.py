"""
test_init_helper.py
懒加载单例模块测试
"""

import pytest
import threading
import time
from jk2bt.utils.init_helper import LazyInitSingleton, make_lazy_init_getter


class TestLazyInitSingleton:
    """测试 LazyInitSingleton 单例"""

    def test_singleton_same_instance(self):
        """测试多次实例化返回同一对象"""

        class TestSingleton(LazyInitSingleton):
            def _do_init(self, value=None):
                self.value = value

        LazyInitSingleton.reset(TestSingleton)

        instance1 = TestSingleton()
        instance2 = TestSingleton()
        assert instance1 is instance2

    def test_init_called_once(self):
        """测试初始化只调用一次"""

        class TestSingleton(LazyInitSingleton):
            init_count = 0

            def _do_init(self, value=None):
                TestSingleton.init_count += 1
                self.value = value

        LazyInitSingleton.reset(TestSingleton)
        TestSingleton.init_count = 0

        instance1 = TestSingleton()
        instance1.ensure_initialized(value=1)
        instance2 = TestSingleton()
        instance2.ensure_initialized(value=2)

        assert TestSingleton.init_count == 1
        assert instance1.value == 1
        assert instance2.value == 1

    def test_thread_safety(self):
        """测试线程安全"""

        class TestSingleton(LazyInitSingleton):
            results = []

            def _do_init(self, delay=0):
                time.sleep(delay)
                TestSingleton.results.append(threading.current_thread().name)

        LazyInitSingleton.reset(TestSingleton)
        TestSingleton.results = []

        def get_instance():
            instance = TestSingleton()
            instance.ensure_initialized(delay=0.1)

        threads = [
            threading.Thread(target=get_instance, name=f"thread_{i}") for i in range(5)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(TestSingleton.results) == 1

    def test_reset_clears_instance(self):
        """测试 reset 清除实例"""

        class TestSingleton(LazyInitSingleton):
            def _do_init(self, value=None):
                self.value = value

        LazyInitSingleton.reset(TestSingleton)

        instance1 = TestSingleton()
        instance1.ensure_initialized(value=42)
        assert instance1.value == 42

        LazyInitSingleton.reset(TestSingleton)

        instance2 = TestSingleton()
        instance2.ensure_initialized(value=100)
        assert instance2.value == 100

    def test_not_implemented_error(self):
        """测试子类未实现 _do_init 时抛异常"""

        class IncompleteSingleton(LazyInitSingleton):
            pass

        LazyInitSingleton.reset(IncompleteSingleton)

        instance = IncompleteSingleton()
        with pytest.raises(NotImplementedError):
            instance.ensure_initialized()


class TestMakeLazyInitGetter:
    """测试懒加载获取函数"""

    def test_getter_returns_manager_when_available(self):
        """测试功能可用时返回管理器"""

        class TestManager(LazyInitSingleton):
            def _do_init(self, db_path=None):
                self.db_path = db_path

        LazyInitSingleton.reset(TestManager)

        getter = make_lazy_init_getter(
            manager_cls=TestManager,
            availability_flag=True,
            default_db_path="/default/path",
        )

        manager = getter()
        assert manager is not None
        assert manager.db_path == "/default/path"

    def test_getter_returns_none_when_unavailable(self):
        """测试功能不可用时返回 None"""

        class TestManager(LazyInitSingleton):
            def _do_init(self, db_path=None):
                self.db_path = db_path

        LazyInitSingleton.reset(TestManager)

        getter = make_lazy_init_getter(
            manager_cls=TestManager,
            availability_flag=False,
            default_db_path="/default/path",
        )

        result = getter()
        assert result is None

    def test_getter_accepts_custom_path(self):
        """测试获取函数接受自定义路径"""

        class TestManager(LazyInitSingleton):
            def _do_init(self, db_path=None):
                self.db_path = db_path

        LazyInitSingleton.reset(TestManager)

        getter = make_lazy_init_getter(
            manager_cls=TestManager,
            availability_flag=True,
            default_db_path="/default/path",
        )

        manager = getter("/custom/path")
        assert manager.db_path == "/custom/path"

    def test_getter_singleton_behavior(self):
        """测试获取函数的单例行为"""

        class TestManager(LazyInitSingleton):
            instance_count = 0

            def _do_init(self, db_path=None):
                TestManager.instance_count += 1
                self.instance_id = TestManager.instance_count

        LazyInitSingleton.reset(TestManager)
        TestManager.instance_count = 0

        getter = make_lazy_init_getter(
            manager_cls=TestManager,
            availability_flag=True,
        )

        manager1 = getter()
        manager2 = getter()

        assert manager1 is manager2
        assert TestManager.instance_count == 1
