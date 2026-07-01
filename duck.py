import duckdb
import os
import sys


def main():
	fname = "relevant_priors_public.json"

	if not os.path.exists(fname):
		print(f"File not found: {fname}", file=sys.stderr)
		sys.exit(1)

	# Try using read_json_auto via SQL (preferred)
	try:
		rel = duckdb.sql(f"SELECT * FROM read_json_auto('{fname}')")
		rows = rel.fetchall()
		print(f"Read {len(rows)} rows from {fname} (read_json_auto)")
		for r in rows[:10]:
			print(r)
		return 0
	except Exception as e:
		print("Primary method (read_json_auto) failed:", e, file=sys.stderr)

	# Fallback: try duckdb.read_json API
	try:
		rel = duckdb.read_json(fname)
		try:
			rows = rel.fetchall()
		except Exception:
			# If it's not a relation, coerce to a list
			rows = list(rel)
		print(f"Read {len(rows)} rows from {fname} (duckdb.read_json)")
		for r in rows[:10]:
			print(r)
		return 0
	except Exception as e:
		print("Fallback method (duckdb.read_json) failed:", e, file=sys.stderr)
		return 1


if __name__ == "__main__":
	raise SystemExit(main())