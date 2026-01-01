using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text.Json;

class Program
{
    static void Main(string[] args)
    {
        Console.WriteLine("C# Basic Operations Benchmark");
        Console.WriteLine("==============================");
        Console.WriteLine();

        var allResults = new List<BenchmarkResult>();

        allResults.AddRange(RunArithmeticBenchmarks());
        Console.WriteLine();

        allResults.AddRange(RunStringBenchmarks());
        Console.WriteLine();

        allResults.AddRange(RunListBenchmarks());
        Console.WriteLine();

        // Output JSON summary
        var summary = new
        {
            language = "C#",
            runtime = ".NET 10.0",
            results = allResults.Select(r => new
            {
                name = r.Name,
                value = r.ValueMs,
                category = r.Category
            })
        };

        Console.WriteLine("JSON Output:");
        Console.WriteLine(JsonSerializer.Serialize(summary, new JsonSerializerOptions
        {
            WriteIndented = true
        }));
    }

    static List<BenchmarkResult> RunArithmeticBenchmarks()
    {
        PrintHeader("Arithmetic Operations");
        var results = new List<BenchmarkResult>();

        // Integer addition
        int aInt = 123, bInt = 456;
        var timeMs = TimeOperationNs(() => { var x = aInt + bInt; }, 100_000);
        PrintResult("Add two integers", timeMs);
        results.Add(new BenchmarkResult("int_add", timeMs, "basic_ops"));

        // Integer multiplication
        timeMs = TimeOperationNs(() => { var x = aInt * bInt; }, 100_000);
        PrintResult("Multiply two integers", timeMs);
        results.Add(new BenchmarkResult("int_multiply", timeMs, "basic_ops"));

        // Integer division
        timeMs = TimeOperationNs(() => { var x = aInt / bInt; }, 100_000);
        PrintResult("Divide two integers", timeMs);
        results.Add(new BenchmarkResult("int_divide", timeMs, "basic_ops"));

        // Float addition
        double aFloat = 123.456, bFloat = 789.012;
        timeMs = TimeOperationNs(() => { var x = aFloat + bFloat; }, 100_000);
        PrintResult("Add two floats", timeMs);
        results.Add(new BenchmarkResult("float_add", timeMs, "basic_ops"));

        // Float multiplication
        timeMs = TimeOperationNs(() => { var x = aFloat * bFloat; }, 100_000);
        PrintResult("Multiply two floats", timeMs);
        results.Add(new BenchmarkResult("float_multiply", timeMs, "basic_ops"));

        // Float division
        timeMs = TimeOperationNs(() => { var x = aFloat / bFloat; }, 100_000);
        PrintResult("Divide two floats", timeMs);
        results.Add(new BenchmarkResult("float_divide", timeMs, "basic_ops"));

        return results;
    }

    static List<BenchmarkResult> RunStringBenchmarks()
    {
        PrintHeader("String Operations");
        var results = new List<BenchmarkResult>();

        // String concatenation (small strings)
        string s1 = "hello", s2 = "world";
        var timeMs = TimeOperationNs(() => { var x = s1 + " " + s2; }, 100_000);
        PrintResult("Concatenation (+) small strings", timeMs);
        results.Add(new BenchmarkResult("concat_small", timeMs, "basic_ops"));

        // String concatenation (medium strings)
        string s1Med = string.Concat(Enumerable.Repeat("hello", 10));
        string s2Med = string.Concat(Enumerable.Repeat("world", 10));
        timeMs = TimeOperationNs(() => { var x = s1Med + " " + s2Med; }, 10_000);
        PrintResult("Concatenation (+) medium strings", timeMs);
        results.Add(new BenchmarkResult("concat_medium", timeMs, "basic_ops"));

        // String interpolation (equivalent to f-string)
        string name = "Alice";
        int age = 30;
        timeMs = TimeOperationNs(() => { var x = $"Hello {name}, you are {age} years old"; }, 100_000);
        PrintResult("String interpolation ($)", timeMs);
        results.Add(new BenchmarkResult("f_string", timeMs, "basic_ops"));

        // String.Format() method
        timeMs = TimeOperationNs(() => { var x = string.Format("Hello {0}, you are {1} years old", name, age); }, 100_000);
        PrintResult("String.Format() method", timeMs);
        results.Add(new BenchmarkResult("format_method", timeMs, "basic_ops"));

        // Composite formatting (using +)
        timeMs = TimeOperationNs(() => { var x = "Hello " + name + ", you are " + age + " years old"; }, 100_000);
        PrintResult("Concatenation formatting", timeMs);
        results.Add(new BenchmarkResult("percent_formatting", timeMs, "basic_ops"));

        // String join (small list)
        var words = new[] { "hello", "world", "python", "test" };
        timeMs = TimeOperationNs(() => { var x = string.Join(" ", words); }, 100_000);
        PrintResult("Join small list", timeMs);
        results.Add(new BenchmarkResult("join_small", timeMs, "basic_ops"));

        // String split
        string sentence = "hello world python test";
        timeMs = TimeOperationNs(() => { var x = sentence.Split(); }, 100_000);
        PrintResult("Split string", timeMs);
        results.Add(new BenchmarkResult("split", timeMs, "basic_ops"));

        return results;
    }

    static List<BenchmarkResult> RunListBenchmarks()
    {
        PrintHeader("List Operations");
        var results = new List<BenchmarkResult>();

        // List add (single item)
        var timeMs = TimeOperation(() =>
        {
            var lst = new List<int>();
            lst.Add(1);
        }, 100_000);
        PrintResult("List.Add() single item", timeMs);
        results.Add(new BenchmarkResult("list_append", timeMs, "basic_ops"));

        // LINQ (10 items)
        timeMs = TimeOperation(() =>
        {
            var lst = Enumerable.Range(0, 10).ToList();
        }, 10_000);
        PrintResult("LINQ Range (10 items)", timeMs);
        results.Add(new BenchmarkResult("list_comp_10", timeMs, "basic_ops"));

        // For-loop (10 items)
        timeMs = TimeOperation(() =>
        {
            var lst = new List<int>();
            for (int i = 0; i < 10; i++)
            {
                lst.Add(i);
            }
        }, 10_000);
        PrintResult("For-loop (10 items)", timeMs);
        results.Add(new BenchmarkResult("for_loop_10", timeMs, "basic_ops"));

        // LINQ (100 items)
        timeMs = TimeOperation(() =>
        {
            var lst = Enumerable.Range(0, 100).ToList();
        }, 10_000);
        PrintResult("LINQ Range (100 items)", timeMs);
        results.Add(new BenchmarkResult("list_comp_100", timeMs, "basic_ops"));

        // For-loop (100 items)
        timeMs = TimeOperation(() =>
        {
            var lst = new List<int>();
            for (int i = 0; i < 100; i++)
            {
                lst.Add(i);
            }
        }, 10_000);
        PrintResult("For-loop (100 items)", timeMs);
        results.Add(new BenchmarkResult("for_loop_100", timeMs, "basic_ops"));

        // LINQ (1000 items)
        timeMs = TimeOperation(() =>
        {
            var lst = Enumerable.Range(0, 1000).ToList();
        }, 1_000);
        PrintResult("LINQ Range (1000 items)", timeMs);
        results.Add(new BenchmarkResult("list_comp_1000", timeMs, "basic_ops"));

        // For-loop (1000 items)
        timeMs = TimeOperation(() =>
        {
            var lst = new List<int>();
            for (int i = 0; i < 1000; i++)
            {
                lst.Add(i);
            }
        }, 1_000);
        PrintResult("For-loop (1000 items)", timeMs);
        results.Add(new BenchmarkResult("for_loop_1000", timeMs, "basic_ops"));

        // List AddRange
        timeMs = TimeOperation(() =>
        {
            var lst1 = new List<int> { 1, 2, 3 };
            var lst2 = new List<int> { 4, 5, 6 };
            lst1.AddRange(lst2);
        }, 100_000);
        PrintResult("List.AddRange() 3 items", timeMs);
        results.Add(new BenchmarkResult("list_extend", timeMs, "basic_ops"));

        // List copy
        var original = Enumerable.Range(0, 100).ToList();
        timeMs = TimeOperation(() =>
        {
            var copy = new List<int>(original);
        }, 10_000);
        PrintResult("List copy (100 items)", timeMs);
        results.Add(new BenchmarkResult("list_copy_100", timeMs, "basic_ops"));

        return results;
    }

    static double TimeOperationNs(Action operation, int iterations)
    {
        // Warmup
        for (int i = 0; i < Math.Min(1000, iterations / 10); i++)
        {
            operation();
        }

        // Force garbage collection before measurement
        GC.Collect();
        GC.WaitForPendingFinalizers();
        GC.Collect();

        var sw = Stopwatch.StartNew();
        for (int i = 0; i < iterations; i++)
        {
            operation();
        }
        sw.Stop();

        // Return milliseconds (nanoseconds / 1,000,000)
        return (sw.Elapsed.TotalNanoseconds / iterations) / 1_000_000.0;
    }

    static double TimeOperation(Action operation, int iterations)
    {
        // Warmup
        for (int i = 0; i < Math.Min(1000, iterations / 10); i++)
        {
            operation();
        }

        // Force garbage collection before measurement
        GC.Collect();
        GC.WaitForPendingFinalizers();
        GC.Collect();

        var sw = Stopwatch.StartNew();
        for (int i = 0; i < iterations; i++)
        {
            operation();
        }
        sw.Stop();

        // Return milliseconds
        return sw.Elapsed.TotalMilliseconds / iterations;
    }

    static void PrintHeader(string title)
    {
        Console.WriteLine($"== {title} ==");
    }

    static void PrintResult(string name, double value)
    {
        Console.WriteLine($"  {name,-40} {value,12:F6} ms");
    }

    record BenchmarkResult(string Name, double ValueMs, string Category);
}
