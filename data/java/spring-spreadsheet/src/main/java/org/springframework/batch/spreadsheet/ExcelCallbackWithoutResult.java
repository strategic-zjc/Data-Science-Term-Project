/*
 * Copyright 2002-2009 the original author or authors.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package org.springframework.batch.spreadsheet;

import org.apache.poi.ss.usermodel.Row;

/**
 * @since 11/2/2009
 * @author Greg Turnquist
 * @see ExcelTemplate
 */
public abstract class ExcelCallbackWithoutResult<T> implements ExcelRowCallback<T> {

	public final T mapRow(Row row) {
		mapRowWithoutResult(row);
		return null;
	}

	protected abstract void mapRowWithoutResult(Row row);

}
