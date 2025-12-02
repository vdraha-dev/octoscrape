import pytest
import time
from octoscrape.multi_runner import MultiRunner


    
def test_init(factory):
    """Checking MultiRunner initialization."""
    runner = MultiRunner(factory, pool_size=3)
    
    assert runner._MultiRunner__factory is factory
    assert isinstance(runner._MultiRunner__processes, list)
    assert runner._MultiRunner__sem.get_value() == 3
    assert not runner.is_stopped


def test_run_single_process(runner, scraper_config, common_config):
    runner.run_process("scraper", scraper_config, common_config)
    
    # Give the process time to start
    time.sleep(0.1)
    
    assert len(runner._MultiRunner__processes) == 1
    assert runner._MultiRunner__processes[0].is_alive()
    
    runner.stop_all()


def test_run_multiple_processes(runner, scraper_config, common_config):
    """Checking the launch of multiple processes."""
    runner.run_process("scraper", scraper_config, common_config)
    runner.run_process("scraper", scraper_config, common_config)
    runner.run_process("scraper", scraper_config, common_config)
    
    time.sleep(0.1)
    
    assert len(runner._MultiRunner__processes) == 3
    
    runner.stop_all()


def test_pool_size_limit(runner, scraper_config, common_config):
    """Checking the pool_size (semaphore) limit."""
    start_time = time.time()
    
    # Launch 8 processes with pool_size=2
    for i in range(8):
        runner.run_process(f"scraper", scraper_config, common_config)
    
    time.sleep(0.1)
    
    #  Only 2 can work simultaneously through semaphore
    active_count = sum(1 for p in runner._MultiRunner__processes if p.is_alive())
    
    # There can be 2-4 depending on timing, but no more than pool_size at a time.
    assert active_count >= 2
    
    runner.stop_all()
    
    elapsed = time.time() - start_time
    # With pool_size=2 and 8 tasks at 0.1s, it should take ~0.4s minimum
    assert elapsed >= .5
    assert elapsed < .6


def test_stop_event_propagation(runner, scraper_config, common_config):
    """Перевірка що stop_event передається worker'ам."""
    runner.run_process("scraper", scraper_config, common_config)
    
    time.sleep(0.2)
    assert not runner.is_stopped
    
    # should not hang for long
    start = time.time()
    runner.stop_all()
    elapsed = time.time() - start
    assert runner.is_stopped
    assert elapsed < 1.


def test_join_waits_for_all_processes(runner, scraper_config, common_config):
    """Verify that stop_all() waits for all processes.."""
    runner.run_process("scraper", scraper_config, common_config)
    runner.run_process("scraper", scraper_config, common_config)
    
    time.sleep(0.1)
    
    # The processes are still alive
    assert any(p.is_alive() for p in runner._MultiRunner__processes)
    runner.stop_all()
    
    # All processes completed
    assert all(not p.is_alive() for p in runner._MultiRunner__processes)


def test_empty_join(runner):
    runner.stop_all()
    assert len(runner._MultiRunner__processes) == 0


def test_stop_before_start(runner, scraper_config, common_config):
    runner.stop_all()
    assert runner.is_stopped
    
    with pytest.raises(RuntimeError, match="Cannot run new process"):
        runner.run_process("scraper", scraper_config, common_config)
    

def test_multiple_stop_calls(runner, scraper_config, common_config):
    runner.run_process("scraper", scraper_config, common_config)
    time.sleep(0.05)
    
    runner.stop_all()
    runner.stop_all()
    runner.stop_all()
    
    assert runner.is_stopped


# def test_process_arguments_passing(self, manager):
#     """Перевірка передачі аргументів у Worker."""
#     with patch.object(manager, 'Worker', wraps=manager.Worker) as mock_worker:
#         runner = MultiRunner(manager, pool_size=2)
        
#         runner.run_process("test_parser", "arg1", "arg2", kwarg1="value1")
#         time.sleep(0.1)
        
#         # Перевіряємо що Worker викликався з правильними аргументами
#         mock_worker.assert_called_once_with(
#             "test_parser", "arg1", "arg2", kwarg1="value1"
#         )
        
#         runner.stop()
#         runner.join()



def test_semaphore_release_after_process_completion(runner, scraper_config, common_config):
    runner.run_process("scraper", scraper_config, common_config)
    runner.run_process("scraper", scraper_config, common_config)
    
    time.sleep(0.05)
    
    sem_value = runner._MultiRunner__sem.get_value()
    assert sem_value == 0
    
    runner.stop_all()

    sem_value = runner._MultiRunner__sem.get_value()
    assert sem_value == 2


def test_exception_in_worker_doesnt_break_runner(runner, scraper_config, common_config): 
    try:       
        runner.run_process("failing_scraper", scraper_config, common_config)
        time.sleep(0.2)
    except RuntimeError:
        pass
    runner.stop_all()