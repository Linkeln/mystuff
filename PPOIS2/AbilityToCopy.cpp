#include <iostream>
#include "Document.h"

namespace AbilityToCopy {
	Document CopyDocument(Document& DocumentToCopy) {
		Document NewDocument;
		NewDocument.name = DocumentToCopy.name + "_copy";
		NewDocument.content = DocumentToCopy.content;
		return NewDocument;
	}
}